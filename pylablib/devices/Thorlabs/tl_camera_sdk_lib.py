# pylint: disable=wrong-spelling-in-comment

from . import tl_camera_sdk_defs  # pylint: disable=unused-import
from .tl_camera_sdk_defs import drtl_error_codes
from .tl_camera_sdk_defs import define_functions

from ...core.utils import ctypes_wrap, py3
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import ctypes
import traceback


class ThorlabsTLCameraError(DeviceError):
    """Generic Thorlabs TLCamera error"""
class ThorlabsTLCameraLibError(ThorlabsTLCameraError):
    """Generic Thorlabs TLCamera library error"""
    def __init__(self, func, code, lib=None):
        self.func=func
        self.code=code
        self.name=drtl_error_codes.get(self.code,"UNKNOWN")
        self.desc=""
        try:
            if lib is not None:
                self.desc=py3.as_str(lib.tl_camera_get_last_error())
        except ThorlabsTLCameraLibError:
            pass
        self.msg="function '{}' raised error {}({}): {}".format(func,code,self.name,self.desc)
        ThorlabsTLCameraError.__init__(self,self.msg)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of Thorlabs TLCamera library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    if passing is None:
        passing={0}
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise ThorlabsTLCameraLibError(func.__name__,result,lib=lib)
        return result
    return errchecker




class ThorlabsTLCameraLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        thorcam_path=load_lib.get_program_files_folder("Thorlabs/Scientific Imaging/ThorCam")
        error_message="The library is automatically supplied with Thorcam software\n"+load_lib.par_error_message.format("thorlabs_tlcam")
        depends=["thorlabs_unified_sdk_kernel.dll","thorlabs_unified_sdk_main.dll",
            "thorlabs_tsi_usb_driver.dll","thorlabs_tsi_usb_driver_libusb.dll","thorlabs_tsi_libusb.dll","thorlabs_tsi_zelux_camera_device.dll",
            "thorlabs_tsi_usb_hotplug_monitor.dll","thorlabs_tsi_cs_camera_device.dll",
            "tsi_sdk.dll","tsi_usb.dll"]
        self.lib=load_lib.load_lib("thorlabs_tsi_camera_sdk.dll",locations=("parameter/thorlabs_tlcam",thorcam_path,"global"),
            depends=depends,depends_required=False,error_message=error_message,call_conv="cdecl")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib=self),default_rvals="pointer")
        max_strlen=4096
        strprep=ctypes_wrap.strprep(max_strlen)

        #  ctypes.c_char_p tl_camera_get_last_error()
        self.tl_camera_get_last_error=ctypes_wrap.CFunctionWrapper()(lib.tl_camera_get_last_error)
        
        #  ctypes.c_int tl_camera_open_sdk()
        self.tl_camera_open_sdk=wrapper(lib.tl_camera_open_sdk)
        #  ctypes.c_int tl_camera_close_sdk()
        self.tl_camera_close_sdk=wrapper(lib.tl_camera_close_sdk)
        #  ctypes.c_int tl_camera_discover_available_cameras(ctypes.c_char_p serial_numbers, ctypes.c_int str_length)
        self.tl_camera_discover_available_cameras=wrapper(lib.tl_camera_discover_available_cameras, args=[], rvals=["serial_numbers"],
            argprep={"serial_numbers":strprep,"str_length":max_strlen}, byref=[])
        #  ctypes.c_int tl_camera_open_camera(ctypes.c_char_p camera_serial_number, ctypes.POINTER(ctypes.c_void_p) tl_camera_handle)
        self.tl_camera_open_camera=wrapper(lib.tl_camera_open_camera)
        #  ctypes.c_int tl_camera_close_camera(ctypes.c_void_p tl_camera_handle)
        self.tl_camera_close_camera=wrapper(lib.tl_camera_close_camera)

        #  ctypes.c_int tl_camera_get_firmware_version(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p firmware_version, ctypes.c_int str_length)
        self.tl_camera_get_firmware_version=wrapper(lib.tl_camera_get_firmware_version, args=["tl_camera_handle"], rvals=["firmware_version"],
            argprep={"firmware_version":strprep, "str_length":max_strlen}, byref=[])
        #  ctypes.c_int tl_camera_get_model_string_length_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) model_min, ctypes.POINTER(ctypes.c_int) model_max)
        self.tl_camera_get_model_string_length_range=wrapper(lib.tl_camera_get_model_string_length_range)
            #  ctypes.c_int tl_camera_get_model(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p model, ctypes.c_int str_length)
        self.tl_camera_get_model=wrapper(lib.tl_camera_get_model, args=["tl_camera_handle"], rvals=["model"],
            argprep={"model":strprep, "str_length":max_strlen}, byref=[])
        #  ctypes.c_int tl_camera_get_name_string_length_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) name_min, ctypes.POINTER(ctypes.c_int) name_max)
        self.tl_camera_get_name_string_length_range=wrapper(lib.tl_camera_get_name_string_length_range)
        #  ctypes.c_int tl_camera_get_name(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p name, ctypes.c_int str_length)
        self.tl_camera_get_name=wrapper(lib.tl_camera_get_name, args=["tl_camera_handle"], rvals=["name"],
            argprep={"name":strprep, "str_length":max_strlen}, byref=[])
        #  ctypes.c_int tl_camera_set_name(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p name)
        self.tl_camera_set_name=wrapper(lib.tl_camera_set_name)
        #  ctypes.c_int tl_camera_get_serial_number_string_length_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) serial_number_min, ctypes.POINTER(ctypes.c_int) serial_number_max)
        self.tl_camera_get_serial_number_string_length_range=wrapper(lib.tl_camera_get_serial_number_string_length_range)
        #  ctypes.c_int tl_camera_get_serial_number(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p serial_number, ctypes.c_int str_length)
        self.tl_camera_get_serial_number=wrapper(lib.tl_camera_get_serial_number, args=["tl_camera_handle"], rvals=["serial_number"],
            argprep={"serial_number":strprep, "str_length":max_strlen}, byref=[])
        #  ctypes.c_int tl_camera_get_usb_port_type(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) usb_port_type)
        self.tl_camera_get_usb_port_type=wrapper(lib.tl_camera_get_usb_port_type)
        #  ctypes.c_int tl_camera_get_communication_interface(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) communication_interface)
        self.tl_camera_get_communication_interface=wrapper(lib.tl_camera_get_communication_interface)
        #  ctypes.c_int tl_camera_get_is_data_rate_supported(ctypes.c_void_p tl_camera_handle, ctypes.c_int data_rate, ctypes.POINTER(ctypes.c_int) is_data_rate_supported)
        self.tl_camera_get_is_data_rate_supported=wrapper(lib.tl_camera_get_is_data_rate_supported)
        #  ctypes.c_int tl_camera_get_is_operation_mode_supported(ctypes.c_void_p tl_camera_handle, ctypes.c_int operation_mode, ctypes.POINTER(ctypes.c_int) is_operation_mode_supported)
        self.tl_camera_get_is_operation_mode_supported=wrapper(lib.tl_camera_get_is_operation_mode_supported)
        #  ctypes.c_int tl_camera_get_is_eep_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_eep_supported)
        self.tl_camera_get_is_eep_supported=wrapper(lib.tl_camera_get_is_eep_supported)
        #  ctypes.c_int tl_camera_get_is_led_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_led_supported)
        self.tl_camera_get_is_led_supported=wrapper(lib.tl_camera_get_is_led_supported)
        #  ctypes.c_int tl_camera_get_is_cooling_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_cooling_supported)
        self.tl_camera_get_is_cooling_supported=wrapper(lib.tl_camera_get_is_cooling_supported)
        #  ctypes.c_int tl_camera_get_is_taps_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_taps_supported, ctypes.c_int tap)
        self.tl_camera_get_is_taps_supported=wrapper(lib.tl_camera_get_is_taps_supported)
        #  ctypes.c_int tl_camera_get_is_nir_boost_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_nir_boost_supported)
        self.tl_camera_get_is_nir_boost_supported=wrapper(lib.tl_camera_get_is_nir_boost_supported)
        #  ctypes.c_int tl_camera_get_camera_sensor_type(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) camera_sensor_type)
        self.tl_camera_get_camera_sensor_type=wrapper(lib.tl_camera_get_camera_sensor_type)
        #  ctypes.c_int tl_camera_get_sensor_pixel_width(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) pixel_width_um)
        self.tl_camera_get_sensor_pixel_width=wrapper(lib.tl_camera_get_sensor_pixel_width)
        #  ctypes.c_int tl_camera_get_sensor_pixel_height(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) pixel_height_um)
        self.tl_camera_get_sensor_pixel_height=wrapper(lib.tl_camera_get_sensor_pixel_height)
        #  ctypes.c_int tl_camera_get_timestamp_clock_frequency(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) timestamp_clock_frequency_hz_or_zero)
        self.tl_camera_get_timestamp_clock_frequency=wrapper(lib.tl_camera_get_timestamp_clock_frequency)
        #  ctypes.c_int tl_camera_get_camera_color_correction_matrix_output_color_space(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p output_color_space)
        self.tl_camera_get_camera_color_correction_matrix_output_color_space=wrapper(lib.tl_camera_get_camera_color_correction_matrix_output_color_space, args=["tl_camera_handle"], rvals=["output_color_space"],
            argprep={"output_color_space":strprep}, byref=[])
        
        #  ctypes.c_int tl_camera_get_exposure_time(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_longlong) exposure_time_us)
        self.tl_camera_get_exposure_time=wrapper(lib.tl_camera_get_exposure_time)
        #  ctypes.c_int tl_camera_set_exposure_time(ctypes.c_void_p tl_camera_handle, ctypes.c_longlong exposure_time_us)
        self.tl_camera_set_exposure_time=wrapper(lib.tl_camera_set_exposure_time)
        #  ctypes.c_int tl_camera_get_exposure_time_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_longlong) exposure_time_us_min, ctypes.POINTER(ctypes.c_longlong) exposure_time_us_max)
        self.tl_camera_get_exposure_time_range=wrapper(lib.tl_camera_get_exposure_time_range)
        #  ctypes.c_int tl_camera_get_image_poll_timeout(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) timeout_ms)
        self.tl_camera_get_image_poll_timeout=wrapper(lib.tl_camera_get_image_poll_timeout)
        #  ctypes.c_int tl_camera_set_image_poll_timeout(ctypes.c_void_p tl_camera_handle, ctypes.c_int timeout_ms)
        self.tl_camera_set_image_poll_timeout=wrapper(lib.tl_camera_set_image_poll_timeout)
        #  ctypes.c_int tl_camera_get_frame_time(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) frame_time_us)
        self.tl_camera_get_frame_time=wrapper(lib.tl_camera_get_frame_time)
        #  ctypes.c_int tl_camera_get_measured_frame_rate(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) frames_per_second)
        self.tl_camera_get_measured_frame_rate=wrapper(lib.tl_camera_get_measured_frame_rate)
        #  ctypes.c_int tl_camera_get_sensor_readout_time(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) sensor_readout_time_ns)
        self.tl_camera_get_sensor_readout_time=wrapper(lib.tl_camera_get_sensor_readout_time)
        #  ctypes.c_int tl_camera_get_data_rate(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) data_rate)
        self.tl_camera_get_data_rate=wrapper(lib.tl_camera_get_data_rate)
        #  ctypes.c_int tl_camera_set_data_rate(ctypes.c_void_p tl_camera_handle, ctypes.c_int data_rate)
        self.tl_camera_set_data_rate=wrapper(lib.tl_camera_set_data_rate)
        #  ctypes.c_int tl_camera_get_eep_status(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) eep_status_enum)
        self.tl_camera_get_eep_status=wrapper(lib.tl_camera_get_eep_status)
        #  ctypes.c_int tl_camera_set_is_eep_enabled(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_eep_enabled)
        self.tl_camera_set_is_eep_enabled=wrapper(lib.tl_camera_set_is_eep_enabled)
        #  ctypes.c_int tl_camera_get_frame_rate_control_value_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) frame_rate_fps_min, ctypes.POINTER(ctypes.c_double) frame_rate_fps_max)
        self.tl_camera_get_frame_rate_control_value_range=wrapper(lib.tl_camera_get_frame_rate_control_value_range)
        #  ctypes.c_int tl_camera_set_frame_rate_control_value(ctypes.c_void_p tl_camera_handle, ctypes.c_double frame_rate_fps)
        self.tl_camera_set_frame_rate_control_value=wrapper(lib.tl_camera_set_frame_rate_control_value)
        #  ctypes.c_int tl_camera_get_is_frame_rate_control_enabled(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_enabled)
        self.tl_camera_get_is_frame_rate_control_enabled=wrapper(lib.tl_camera_get_is_frame_rate_control_enabled)
        #  ctypes.c_int tl_camera_set_is_frame_rate_control_enabled(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_enabled)
        self.tl_camera_set_is_frame_rate_control_enabled=wrapper(lib.tl_camera_set_is_frame_rate_control_enabled)
        
        #  ctypes.c_int tl_camera_get_trigger_polarity(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) trigger_polarity_enum)
        self.tl_camera_get_trigger_polarity=wrapper(lib.tl_camera_get_trigger_polarity)
        #  ctypes.c_int tl_camera_set_trigger_polarity(ctypes.c_void_p tl_camera_handle, ctypes.c_int trigger_polarity_enum)
        self.tl_camera_set_trigger_polarity=wrapper(lib.tl_camera_set_trigger_polarity)
        #  ctypes.c_int tl_camera_get_frames_per_trigger_zero_for_unlimited(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_uint) number_of_frames_per_trigger_or_zero_for_unlimited)
        self.tl_camera_get_frames_per_trigger_zero_for_unlimited=wrapper(lib.tl_camera_get_frames_per_trigger_zero_for_unlimited)
        #  ctypes.c_int tl_camera_set_frames_per_trigger_zero_for_unlimited(ctypes.c_void_p tl_camera_handle, ctypes.c_uint number_of_frames_per_trigger_or_zero_for_unlimited)
        self.tl_camera_set_frames_per_trigger_zero_for_unlimited=wrapper(lib.tl_camera_set_frames_per_trigger_zero_for_unlimited)
        #  ctypes.c_int tl_camera_get_frames_per_trigger_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_uint) number_of_frames_per_trigger_min, ctypes.POINTER(ctypes.c_uint) number_of_frames_per_trigger_max)
        self.tl_camera_get_frames_per_trigger_range=wrapper(lib.tl_camera_get_frames_per_trigger_range)
        #  ctypes.c_int tl_camera_get_operation_mode(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) operation_mode)
        self.tl_camera_get_operation_mode=wrapper(lib.tl_camera_get_operation_mode)
        #  ctypes.c_int tl_camera_set_operation_mode(ctypes.c_void_p tl_camera_handle, ctypes.c_int operation_mode)
        self.tl_camera_set_operation_mode=wrapper(lib.tl_camera_set_operation_mode)
        
        #  ctypes.c_int tl_camera_get_binx_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) hbin_min, ctypes.POINTER(ctypes.c_int) hbin_max)
        self.tl_camera_get_binx_range=wrapper(lib.tl_camera_get_binx_range)
        #  ctypes.c_int tl_camera_get_binx(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) binx)
        self.tl_camera_get_binx=wrapper(lib.tl_camera_get_binx)
        #  ctypes.c_int tl_camera_set_binx(ctypes.c_void_p tl_camera_handle, ctypes.c_int binx)
        self.tl_camera_set_binx=wrapper(lib.tl_camera_set_binx)
        #  ctypes.c_int tl_camera_get_biny_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) vbin_min, ctypes.POINTER(ctypes.c_int) vbin_max)
        self.tl_camera_get_biny_range=wrapper(lib.tl_camera_get_biny_range)
        #  ctypes.c_int tl_camera_get_biny(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) biny)
        self.tl_camera_get_biny=wrapper(lib.tl_camera_get_biny)
        #  ctypes.c_int tl_camera_set_biny(ctypes.c_void_p tl_camera_handle, ctypes.c_int biny)
        self.tl_camera_set_biny=wrapper(lib.tl_camera_set_biny)
        #  ctypes.c_int tl_camera_get_image_width(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) width_pixels)
        self.tl_camera_get_image_width=wrapper(lib.tl_camera_get_image_width)
        #  ctypes.c_int tl_camera_get_image_height(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) height_pixels)
        self.tl_camera_get_image_height=wrapper(lib.tl_camera_get_image_height)
        #  ctypes.c_int tl_camera_get_sensor_width(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) width_pixels)
        self.tl_camera_get_sensor_width=wrapper(lib.tl_camera_get_sensor_width)
        #  ctypes.c_int tl_camera_get_sensor_height(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) height_pixels)
        self.tl_camera_get_sensor_height=wrapper(lib.tl_camera_get_sensor_height)
        #  ctypes.c_int tl_camera_get_image_width_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) image_width_pixels_min, ctypes.POINTER(ctypes.c_int) image_width_pixels_max)
        self.tl_camera_get_image_width_range=wrapper(lib.tl_camera_get_image_width_range)
        #  ctypes.c_int tl_camera_get_image_height_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) image_height_pixels_min, ctypes.POINTER(ctypes.c_int) image_height_pixels_max)
        self.tl_camera_get_image_height_range=wrapper(lib.tl_camera_get_image_height_range)
        #  ctypes.c_int tl_camera_get_roi(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) upper_left_x_pixels, ctypes.POINTER(ctypes.c_int) upper_left_y_pixels, ctypes.POINTER(ctypes.c_int) lower_right_x_pixels, ctypes.POINTER(ctypes.c_int) lower_right_y_pixels)
        self.tl_camera_get_roi=wrapper(lib.tl_camera_get_roi)
        #  ctypes.c_int tl_camera_set_roi(ctypes.c_void_p tl_camera_handle, ctypes.c_int upper_left_x_pixels, ctypes.c_int upper_left_y_pixels, ctypes.c_int lower_right_x_pixels, ctypes.c_int lower_right_y_pixels)
        self.tl_camera_set_roi=wrapper(lib.tl_camera_set_roi)
        #  ctypes.c_int tl_camera_get_roi_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) upper_left_x_pixels_min, ctypes.POINTER(ctypes.c_int) upper_left_y_pixels_min, ctypes.POINTER(ctypes.c_int) lower_right_x_pixels_min, ctypes.POINTER(ctypes.c_int) lower_right_y_pixels_min, ctypes.POINTER(ctypes.c_int) upper_left_x_pixels_max, ctypes.POINTER(ctypes.c_int) upper_left_y_pixels_max, ctypes.POINTER(ctypes.c_int) lower_right_x_pixels_max, ctypes.POINTER(ctypes.c_int) lower_right_y_pixels_max)
        self.tl_camera_get_roi_range=wrapper(lib.tl_camera_get_roi_range)
        
        #  ctypes.c_int tl_camera_get_is_hot_pixel_correction_enabled(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_hot_pixel_correction_enabled)
        self.tl_camera_get_is_hot_pixel_correction_enabled=wrapper(lib.tl_camera_get_is_hot_pixel_correction_enabled)
        #  ctypes.c_int tl_camera_set_is_hot_pixel_correction_enabled(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_hot_pixel_correction_enabled)
        self.tl_camera_set_is_hot_pixel_correction_enabled=wrapper(lib.tl_camera_set_is_hot_pixel_correction_enabled)
        #  ctypes.c_int tl_camera_get_hot_pixel_correction_threshold_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) hot_pixel_correction_threshold_min, ctypes.POINTER(ctypes.c_int) hot_pixel_correction_threshold_max)
        self.tl_camera_get_hot_pixel_correction_threshold_range=wrapper(lib.tl_camera_get_hot_pixel_correction_threshold_range)
        #  ctypes.c_int tl_camera_get_hot_pixel_correction_threshold(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) hot_pixel_correction_threshold)
        self.tl_camera_get_hot_pixel_correction_threshold=wrapper(lib.tl_camera_get_hot_pixel_correction_threshold)
        #  ctypes.c_int tl_camera_set_hot_pixel_correction_threshold(ctypes.c_void_p tl_camera_handle, ctypes.c_int hot_pixel_correction_threshold)
        self.tl_camera_set_hot_pixel_correction_threshold=wrapper(lib.tl_camera_set_hot_pixel_correction_threshold)
        #  ctypes.c_int tl_camera_get_gain_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) gain_min, ctypes.POINTER(ctypes.c_int) gain_max)
        self.tl_camera_get_gain_range=wrapper(lib.tl_camera_get_gain_range)
        #  ctypes.c_int tl_camera_get_gain(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) gain)
        self.tl_camera_get_gain=wrapper(lib.tl_camera_get_gain)
        #  ctypes.c_int tl_camera_set_gain(ctypes.c_void_p tl_camera_handle, ctypes.c_int gain)
        self.tl_camera_set_gain=wrapper(lib.tl_camera_set_gain)
        #  ctypes.c_int tl_camera_get_polar_phase(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) polar_phase)
        self.tl_camera_get_polar_phase=wrapper(lib.tl_camera_get_polar_phase)
        #  ctypes.c_int tl_camera_get_taps(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) taps)
        self.tl_camera_get_taps=wrapper(lib.tl_camera_get_taps)
        #  ctypes.c_int tl_camera_set_taps(ctypes.c_void_p tl_camera_handle, ctypes.c_int taps)
        self.tl_camera_set_taps=wrapper(lib.tl_camera_set_taps)
        #  ctypes.c_int tl_camera_get_tap_balance_enable(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) taps_balance_enable)
        self.tl_camera_get_tap_balance_enable=wrapper(lib.tl_camera_get_tap_balance_enable)
        #  ctypes.c_int tl_camera_set_tap_balance_enable(ctypes.c_void_p tl_camera_handle, ctypes.c_int taps_balance_enable)
        self.tl_camera_set_tap_balance_enable=wrapper(lib.tl_camera_set_tap_balance_enable)
        #  ctypes.c_int tl_camera_get_nir_boost_enable(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) nir_boost_enable)
        self.tl_camera_get_nir_boost_enable=wrapper(lib.tl_camera_get_nir_boost_enable)
        #  ctypes.c_int tl_camera_set_nir_boost_enable(ctypes.c_void_p tl_camera_handle, ctypes.c_int nir_boost_enable)
        self.tl_camera_set_nir_boost_enable=wrapper(lib.tl_camera_set_nir_boost_enable)
        #  ctypes.c_int tl_camera_get_cooling_enable(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_cooling_enabled)
        self.tl_camera_get_cooling_enable=wrapper(lib.tl_camera_get_cooling_enable)
        #  ctypes.c_int tl_camera_set_cooling_enable(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_cooling_enabled)
        self.tl_camera_set_cooling_enable=wrapper(lib.tl_camera_set_cooling_enable)
        #  ctypes.c_int tl_camera_get_is_led_on(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_led_on)
        self.tl_camera_get_is_led_on=wrapper(lib.tl_camera_get_is_led_on)
        #  ctypes.c_int tl_camera_set_is_led_on(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_led_on)
        self.tl_camera_set_is_led_on=wrapper(lib.tl_camera_set_is_led_on)
        #  ctypes.c_int tl_camera_get_black_level_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) min, ctypes.POINTER(ctypes.c_int) max)
        self.tl_camera_get_black_level_range=wrapper(lib.tl_camera_get_black_level_range)
        #  ctypes.c_int tl_camera_get_black_level(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) black_level)
        self.tl_camera_get_black_level=wrapper(lib.tl_camera_get_black_level)
        #  ctypes.c_int tl_camera_set_black_level(ctypes.c_void_p tl_camera_handle, ctypes.c_int black_level)
        self.tl_camera_set_black_level=wrapper(lib.tl_camera_set_black_level)
        
        #  ctypes.c_int tl_camera_get_default_white_balance_matrix(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_float) matrix)
        self.tl_camera_get_default_white_balance_matrix=wrapper(lib.tl_camera_get_default_white_balance_matrix,
            argprep={"matrix":(ctypes.c_float*9)()}, rconv={"matrix": lambda v: v[:9]}, byref=[])
        #  ctypes.c_int tl_camera_get_color_correction_matrix(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_float) matrix)
        self.tl_camera_get_color_correction_matrix=wrapper(lib.tl_camera_get_color_correction_matrix,
            argprep={"matrix":(ctypes.c_float*9)()}, rconv={"matrix": lambda v: v[:9]}, byref=[])
        #  ctypes.c_int tl_camera_get_color_filter_array_phase(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) cfaPhase)
        self.tl_camera_get_color_filter_array_phase=wrapper(lib.tl_camera_get_color_filter_array_phase)
        
        #  ctypes.c_int tl_camera_arm(ctypes.c_void_p tl_camera_handle, ctypes.c_int number_of_frames_to_buffer)
        self.tl_camera_arm=wrapper(lib.tl_camera_arm)
        #  ctypes.c_int tl_camera_issue_software_trigger(ctypes.c_void_p tl_camera_handle)
        self.tl_camera_issue_software_trigger=wrapper(lib.tl_camera_issue_software_trigger)
        #  ctypes.c_int tl_camera_disarm(ctypes.c_void_p tl_camera_handle)
        self.tl_camera_disarm=wrapper(lib.tl_camera_disarm)
        #  ctypes.c_int tl_camera_get_is_armed(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_armed)
        self.tl_camera_get_is_armed=wrapper(lib.tl_camera_get_is_armed)
        
        #  ctypes.c_int tl_camera_get_sensor_pixel_size_bytes(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) sensor_pixel_size_bytes)
        self.tl_camera_get_sensor_pixel_size_bytes=wrapper(lib.tl_camera_get_sensor_pixel_size_bytes)
        #  ctypes.c_int tl_camera_get_bit_depth(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) pixel_bit_depth)
        self.tl_camera_get_bit_depth=wrapper(lib.tl_camera_get_bit_depth)
        #  ctypes.c_int tl_camera_get_pending_frame_or_null(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.POINTER(ctypes.c_ushort)) image_buffer, ctypes.POINTER(ctypes.c_int) frame_count, ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte)) metadata, ctypes.POINTER(ctypes.c_int) metadata_size_in_bytes)
        self.tl_camera_get_pending_frame_or_null=wrapper(lib.tl_camera_get_pending_frame_or_null)

        #  ctypes.c_int tl_camera_get_frame_available_callback(ctypes.c_void_p tl_camera_handle, ctypes.c_void_p handler)
        self.tl_camera_get_frame_available_callback=wrapper(lib.tl_camera_get_frame_available_callback)
        #  ctypes.c_int tl_camera_set_frame_available_callback(ctypes.c_void_p tl_camera_handle, TL_CAMERA_FRAME_AVAILABLE_CALLBACK handler, ctypes.c_void_p context)
        self.c_frame_available_callback=ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort), ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)
        self.tl_camera_set_frame_available_callback_lib=wrapper(lib.tl_camera_set_frame_available_callback)
        #  ctypes.c_int tl_camera_set_camera_connect_callback(TL_CAMERA_CONNECT_CALLBACK handler, ctypes.c_void_p context)
        self.c_camera_connect_callback=ctypes.WINFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p)
        self.tl_camera_set_camera_connect_callback_lib=wrapper(lib.tl_camera_set_camera_connect_callback)
        #  ctypes.c_int tl_camera_set_camera_disconnect_callback(TL_CAMERA_DISCONNECT_CALLBACK handler, ctypes.c_void_p context)
        self.c_camera_disconnect_callback=ctypes.WINFUNCTYPE(None, ctypes.c_char_p, ctypes.c_void_p)
        self.tl_camera_set_camera_disconnect_callback_lib=wrapper(lib.tl_camera_set_camera_disconnect_callback)
        
        #  ctypes.c_int tl_camera_convert_gain_to_decibels(ctypes.c_void_p tl_camera_handle, ctypes.c_int index_of_gain_value, ctypes.POINTER(ctypes.c_double) gain_dB)
        self.tl_camera_convert_gain_to_decibels=wrapper(lib.tl_camera_convert_gain_to_decibels)
        #  ctypes.c_int tl_camera_convert_decibels_to_gain(ctypes.c_void_p tl_camera_handle, ctypes.c_double gain_dB, ctypes.POINTER(ctypes.c_int) index_of_gain_value)
        self.tl_camera_convert_decibels_to_gain=wrapper(lib.tl_camera_convert_decibels_to_gain)
        
        self._initialized=True

        return

        ### Undocumented ###
        #  ctypes.c_int _internal_command(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p data, ctypes.c_char_p response, ctypes.c_int response_size)



    def _wrap_callback(self, callback, callback_type, wrap=True):
        if callback is None:
            return None
        if wrap:
            def wrapped_callback(*args):
                try:
                    callback(*args)
                except: # pylint: disable=bare-except
                    traceback.print_exc()
            return callback_type(wrapped_callback)
        else:
            return callback_type(callback)
    def tl_camera_set_frame_available_callback(self, tl_camera_handle, handler, context=None, wrap=True):
        cb=self._wrap_callback(handler,self.c_frame_available_callback,wrap=wrap)
        self.tl_camera_set_frame_available_callback_lib(tl_camera_handle,cb,context)
        return cb
    def tl_camera_set_camera_connect_callback(self, handler, context=None, wrap=True):
        cb=self._wrap_callback(handler,self.c_camera_connect_callback,wrap=wrap)
        self.tl_camera_set_camera_connect_callback_lib(cb,context)
        return cb
    def tl_camera_set_camera_disconnect_callback(self, handler, context=None, wrap=True):
        cb=self._wrap_callback(handler,self.c_camera_disconnect_callback,wrap=wrap)
        self.tl_camera_set_camera_disconnect_callback_lib(cb,context)
        return cb



wlib=ThorlabsTLCameraLib()