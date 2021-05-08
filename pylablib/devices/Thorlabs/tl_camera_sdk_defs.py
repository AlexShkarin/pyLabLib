##########   This file is generated automatically based on tl_camera_sdk.h, thorlabs_unified_sdk_error.h, tl_color_error.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### TYPE DEFINITIONS #####


BYTE=ctypes.c_ubyte
PBYTE=ctypes.POINTER(BYTE)
CHAR=ctypes.c_char
PCHAR=ctypes.c_char_p
UCHAR=ctypes.c_ubyte
PUCHAR=ctypes.POINTER(UCHAR)
ULONG_PTR=ctypes.c_uint64
LONG_PTR=ctypes.c_int64
WORD=ctypes.c_ushort
LPWORD=ctypes.POINTER(WORD)
LONGLONG=ctypes.c_int64
LPLONG=ctypes.POINTER(ctypes.c_long)
HANDLE=ctypes.c_void_p
LPHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
TL_CAMERA_FRAME_AVAILABLE_CALLBACK=ctypes.c_void_p
TL_CAMERA_CONNECT_CALLBACK=ctypes.c_void_p
TL_CAMERA_DISCONNECT_CALLBACK=ctypes.c_void_p
class TL_COLOR_FILTER_ARRAY_PHASE(enum.IntEnum):
    TL_COLOR_FILTER_ARRAY_PHASE_BAYER_RED               =_int32(0)
    TL_COLOR_FILTER_ARRAY_PHASE_BAYER_BLUE              =enum.auto()
    TL_COLOR_FILTER_ARRAY_PHASE_BAYER_GREEN_LEFT_OF_RED =enum.auto()
    TL_COLOR_FILTER_ARRAY_PHASE_BAYER_GREEN_LEFT_OF_BLUE=enum.auto()
    TL_COLOR_FILTER_ARRAY_PHASE_MAX                     =enum.auto()
dTL_COLOR_FILTER_ARRAY_PHASE={a.name:a.value for a in TL_COLOR_FILTER_ARRAY_PHASE}
drTL_COLOR_FILTER_ARRAY_PHASE={a.value:a.name for a in TL_COLOR_FILTER_ARRAY_PHASE}


class TL_COLOR_FORMAT(enum.IntEnum):
    TL_COLOR_FORMAT_BGR_PLANAR=_int32(0)
    TL_COLOR_FORMAT_BGR_PIXEL =enum.auto()
    TL_COLOR_FORMAT_RGB_PIXEL =enum.auto()
    TL_COLOR_FORMAT_MAX       =enum.auto()
dTL_COLOR_FORMAT={a.name:a.value for a in TL_COLOR_FORMAT}
drTL_COLOR_FORMAT={a.value:a.name for a in TL_COLOR_FORMAT}


class TL_COLOR_FILTER_TYPE(enum.IntEnum):
    TL_COLOR_FILTER_TYPE_BAYER=_int32(0)
    TL_COLOR_FILTER_TYPE_MAX  =enum.auto()
dTL_COLOR_FILTER_TYPE={a.name:a.value for a in TL_COLOR_FILTER_TYPE}
drTL_COLOR_FILTER_TYPE={a.value:a.name for a in TL_COLOR_FILTER_TYPE}


class TL_POLARIZATION_PROCESSOR_POLAR_PHASE(enum.IntEnum):
    TL_POLARIZATION_PROCESSOR_POLAR_PHASE_0_DEGREES  =_int32(0)
    TL_POLARIZATION_PROCESSOR_POLAR_PHASE_45_DEGREES =enum.auto()
    TL_POLARIZATION_PROCESSOR_POLAR_PHASE_90_DEGREES =enum.auto()
    TL_POLARIZATION_PROCESSOR_POLAR_PHASE_135_DEGREES=enum.auto()
    TL_POLARIZATION_PROCESSOR_POLAR_PHASE_MAX        =enum.auto()
dTL_POLARIZATION_PROCESSOR_POLAR_PHASE={a.name:a.value for a in TL_POLARIZATION_PROCESSOR_POLAR_PHASE}
drTL_POLARIZATION_PROCESSOR_POLAR_PHASE={a.value:a.name for a in TL_POLARIZATION_PROCESSOR_POLAR_PHASE}


class TL_CAMERA_ERROR(enum.IntEnum):
    TL_CAMERA_ERROR_NONE                  =_int32(0)
    TL_CAMERA_ERROR_COMMAND_NOT_FOUND     =enum.auto()
    TL_CAMERA_ERROR_TOO_MANY_ARGUMENTS    =enum.auto()
    TL_CAMERA_ERROR_NOT_ENOUGH_ARGUMENTS  =enum.auto()
    TL_CAMERA_ERROR_INVALID_COMMAND       =enum.auto()
    TL_CAMERA_ERROR_DUPLICATE_COMMAND     =enum.auto()
    TL_CAMERA_ERROR_MISSING_JSON_COMMAND  =enum.auto()
    TL_CAMERA_ERROR_INITIALIZING          =enum.auto()
    TL_CAMERA_ERROR_NOTSUPPORTED          =enum.auto()
    TL_CAMERA_ERROR_FPGA_NOT_PROGRAMMED   =enum.auto()
    TL_CAMERA_ERROR_ROI_WIDTH_ERROR       =enum.auto()
    TL_CAMERA_ERROR_ROI_RANGE_ERROR       =enum.auto()
    TL_CAMERA_ERROR_RANGE_ERROR           =enum.auto()
    TL_CAMERA_ERROR_COMMAND_LOCKED        =enum.auto()
    TL_CAMERA_ERROR_CAMERA_MUST_BE_STOPPED=enum.auto()
    TL_CAMERA_ERROR_ROI_BIN_COMBO_ERROR   =enum.auto()
    TL_CAMERA_ERROR_IMAGE_DATA_SYNC_ERROR =enum.auto()
    TL_CAMERA_ERROR_MAX_ERRORS            =enum.auto()
dTL_CAMERA_ERROR={a.name:a.value for a in TL_CAMERA_ERROR}
drTL_CAMERA_ERROR={a.value:a.name for a in TL_CAMERA_ERROR}


class TL_CAMERA_OPERATION_MODE(enum.IntEnum):
    TL_CAMERA_OPERATION_MODE_SOFTWARE_TRIGGERED=_int32(0)
    TL_CAMERA_OPERATION_MODE_HARDWARE_TRIGGERED=enum.auto()
    TL_CAMERA_OPERATION_MODE_BULB              =enum.auto()
    TL_CAMERA_OPERATION_MODE_RESERVED1         =enum.auto()
    TL_CAMERA_OPERATION_MODE_RESERVED2         =enum.auto()
    TL_CAMERA_OPERATION_MODE_MAX               =enum.auto()
dTL_CAMERA_OPERATION_MODE={a.name:a.value for a in TL_CAMERA_OPERATION_MODE}
drTL_CAMERA_OPERATION_MODE={a.value:a.name for a in TL_CAMERA_OPERATION_MODE}


class TL_CAMERA_SENSOR_TYPE(enum.IntEnum):
    TL_CAMERA_SENSOR_TYPE_MONOCHROME          =_int32(0)
    TL_CAMERA_SENSOR_TYPE_BAYER               =enum.auto()
    TL_CAMERA_SENSOR_TYPE_MONOCHROME_POLARIZED=enum.auto()
    TL_CAMERA_SENSOR_TYPE_MAX                 =enum.auto()
dTL_CAMERA_SENSOR_TYPE={a.name:a.value for a in TL_CAMERA_SENSOR_TYPE}
drTL_CAMERA_SENSOR_TYPE={a.value:a.name for a in TL_CAMERA_SENSOR_TYPE}


class TL_CAMERA_TRIGGER_POLARITY(enum.IntEnum):
    TL_CAMERA_TRIGGER_POLARITY_ACTIVE_HIGH=_int32(0)
    TL_CAMERA_TRIGGER_POLARITY_ACTIVE_LOW =enum.auto()
    TL_CAMERA_TRIGGER_POLARITY_MAX        =enum.auto()
dTL_CAMERA_TRIGGER_POLARITY={a.name:a.value for a in TL_CAMERA_TRIGGER_POLARITY}
drTL_CAMERA_TRIGGER_POLARITY={a.value:a.name for a in TL_CAMERA_TRIGGER_POLARITY}


class TL_CAMERA_EEP_STATUS(enum.IntEnum):
    TL_CAMERA_EEP_STATUS_DISABLED        =_int32(0)
    TL_CAMERA_EEP_STATUS_ENABLED_ACTIVE  =enum.auto()
    TL_CAMERA_EEP_STATUS_ENABLED_INACTIVE=enum.auto()
    TL_CAMERA_EEP_STATUS_ENABLED_BULB    =enum.auto()
    TL_CAMERA_EEP_STATUS_MAX             =enum.auto()
dTL_CAMERA_EEP_STATUS={a.name:a.value for a in TL_CAMERA_EEP_STATUS}
drTL_CAMERA_EEP_STATUS={a.value:a.name for a in TL_CAMERA_EEP_STATUS}


class TL_CAMERA_DATA_RATE(enum.IntEnum):
    TL_CAMERA_DATA_RATE_READOUT_FREQUENCY_20=_int32(0)
    TL_CAMERA_DATA_RATE_READOUT_FREQUENCY_40=enum.auto()
    TL_CAMERA_DATA_RATE_FPS_30              =enum.auto()
    TL_CAMERA_DATA_RATE_FPS_50              =enum.auto()
    TL_CAMERA_DATA_RATE_MAX                 =enum.auto()
dTL_CAMERA_DATA_RATE={a.name:a.value for a in TL_CAMERA_DATA_RATE}
drTL_CAMERA_DATA_RATE={a.value:a.name for a in TL_CAMERA_DATA_RATE}


class TL_CAMERA_USB_PORT_TYPE(enum.IntEnum):
    TL_CAMERA_USB_PORT_TYPE_USB1_0=_int32(0)
    TL_CAMERA_USB_PORT_TYPE_USB2_0=enum.auto()
    TL_CAMERA_USB_PORT_TYPE_USB3_0=enum.auto()
    TL_CAMERA_USB_PORT_TYPE_MAX   =enum.auto()
dTL_CAMERA_USB_PORT_TYPE={a.name:a.value for a in TL_CAMERA_USB_PORT_TYPE}
drTL_CAMERA_USB_PORT_TYPE={a.value:a.name for a in TL_CAMERA_USB_PORT_TYPE}


class TL_CAMERA_TAPS(enum.IntEnum):
    TL_CAMERA_TAPS_SINGLE_TAP=_int32(0)
    TL_CAMERA_TAPS_DUAL_TAP  =_int32(1)
    TL_CAMERA_TAPS_QUAD_TAP  =_int32(2)
    TL_CAMERA_TAPS_MAX_TAP   =_int32(3)
dTL_CAMERA_TAPS={a.name:a.value for a in TL_CAMERA_TAPS}
drTL_CAMERA_TAPS={a.value:a.name for a in TL_CAMERA_TAPS}


class TL_CAMERA_COMMUNICATION_INTERFACE(enum.IntEnum):
    TL_CAMERA_COMMUNICATION_INTERFACE_GIG_E      =_int32(0)
    TL_CAMERA_COMMUNICATION_INTERFACE_CAMERA_LINK=_int32(1)
    TL_CAMERA_COMMUNICATION_INTERFACE_USB        =_int32(2)
    TL_CAMERA_COMMUNICATION_INTERFACE_MAX        =_int32(3)
dTL_CAMERA_COMMUNICATION_INTERFACE={a.name:a.value for a in TL_CAMERA_COMMUNICATION_INTERFACE}
drTL_CAMERA_COMMUNICATION_INTERFACE={a.value:a.name for a in TL_CAMERA_COMMUNICATION_INTERFACE}


class tl_error_codes(enum.IntEnum):
    TL_NO_ERROR                             =_int32(0)
    TL_MEMORY_DEALLOCATE_ERROR              =enum.auto()
    TL_TOO_MANY_INTERNAL_FUNCTIONS_REQUESTED=enum.auto()
    TL_FAILED_TO_OPEN_MODULE                =enum.auto()
    TL_FAILED_TO_MAP_FUNCTION               =enum.auto()
    TL_OBJECT_NOT_FOUND                     =enum.auto()
    TL_GET_DATA_FAILED                      =enum.auto()
    TL_SET_DATA_FAILED                      =enum.auto()
    TL_INITIALIZATION_FAILURE               =enum.auto()
    TL_FAILED_TO_OPEN_DEVICE                =enum.auto()
    TL_FAILED_TO_CLOSE_DEVICE               =enum.auto()
    TL_FAILED_TO_START_DEVICE               =enum.auto()
    TL_FAILED_TO_STOP_DEVICE                =enum.auto()
    TL_COMMUNICATION_FAILURE                =enum.auto()
    TL_DEVICE_DISCONNECTED                  =enum.auto()
    TL_INSUFFICIENT_BUFFER_SIZE             =enum.auto()
    TL_INVALID_POINTER                      =enum.auto()
    TL_ERROR_MAX                            =enum.auto()
dtl_error_codes={a.name:a.value for a in tl_error_codes}
drtl_error_codes={a.value:a.name for a in tl_error_codes}


class TL_COLOR_ERROR(enum.IntEnum):
    TL_COLOR_NO_ERROR                          =_int32(0)
    TL_COLOR_MODULE_NOT_INITIALIZED            =enum.auto()
    TL_COLOR_NULL_INSTANCE_HANDLE              =enum.auto()
    TL_COLOR_NULL_INPUT_BUFFER_POINTER         =enum.auto()
    TL_COLOR_NULL_OUTPUT_BUFFER_POINTER        =enum.auto()
    TL_COLOR_IDENTICAL_INPUT_AND_OUTPUT_BUFFERS=enum.auto()
    TL_COLOR_INVALID_COLOR_FILTER_ARRAY_PHASE  =enum.auto()
    TL_COLOR_INVALID_COLOR_FILTER_TYPE         =enum.auto()
    TL_COLOR_INVALID_BIT_DEPTH                 =enum.auto()
    TL_COLOR_INVALID_INPUT_COLOR_FORMAT        =enum.auto()
    TL_COLOR_INVALID_OUTPUT_COLOR_FORMAT       =enum.auto()
    TL_COLOR_INVALID_BIT_SHIFT_DISTANCE        =enum.auto()
    TL_COLOR_INVALID_CLAMP_VALUE               =enum.auto()
dTL_COLOR_ERROR={a.name:a.value for a in TL_COLOR_ERROR}
drTL_COLOR_ERROR={a.value:a.name for a in TL_COLOR_ERROR}





##### FUNCTION DEFINITIONS #####





def addfunc(lib, name, restype, argtypes=None, argnames=None):
    if getattr(lib,name,None) is None:
        setattr(lib,name,None)
    else:
        func=getattr(lib,name)
        func.restype=restype
        if argtypes is not None:
            func.argtypes=argtypes
        if argnames is not None:
            func.argnames=argnames

def define_functions(lib):
    #  None tl_camera_frame_available_callback(ctypes.c_void_p sender, ctypes.POINTER(ctypes.c_ushort) image_buffer, ctypes.c_int frame_count, ctypes.POINTER(ctypes.c_ubyte) metadata, ctypes.c_int metadata_size_in_bytes, ctypes.c_void_p context)
    addfunc(lib, "tl_camera_frame_available_callback", restype = None,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort), ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.c_void_p],
            argnames = ["sender", "image_buffer", "frame_count", "metadata", "metadata_size_in_bytes", "context"] )
    #  None tl_camera_connect_callback(ctypes.c_char_p cameraSerialNumber, ctypes.c_int usb_port_type, ctypes.c_void_p context)
    addfunc(lib, "tl_camera_connect_callback", restype = None,
            argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p],
            argnames = ["cameraSerialNumber", "usb_port_type", "context"] )
    #  None tl_camera_disconnect_callback(ctypes.c_char_p cameraSerialNumber, ctypes.c_void_p context)
    addfunc(lib, "tl_camera_disconnect_callback", restype = None,
            argtypes = [ctypes.c_char_p, ctypes.c_void_p],
            argnames = ["cameraSerialNumber", "context"] )
    #  ctypes.c_int tl_camera_get_frame_available_callback(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(TL_CAMERA_FRAME_AVAILABLE_CALLBACK) handler)
    addfunc(lib, "tl_camera_get_frame_available_callback", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(TL_CAMERA_FRAME_AVAILABLE_CALLBACK)],
            argnames = ["tl_camera_handle", "handler"] )
    #  ctypes.c_int tl_camera_set_frame_available_callback(ctypes.c_void_p tl_camera_handle, TL_CAMERA_FRAME_AVAILABLE_CALLBACK handler, ctypes.c_void_p context)
    addfunc(lib, "tl_camera_set_frame_available_callback", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, TL_CAMERA_FRAME_AVAILABLE_CALLBACK, ctypes.c_void_p],
            argnames = ["tl_camera_handle", "handler", "context"] )
    #  ctypes.c_int tl_camera_set_camera_connect_callback(TL_CAMERA_CONNECT_CALLBACK handler, ctypes.c_void_p context)
    addfunc(lib, "tl_camera_set_camera_connect_callback", restype = ctypes.c_int,
            argtypes = [TL_CAMERA_CONNECT_CALLBACK, ctypes.c_void_p],
            argnames = ["handler", "context"] )
    #  ctypes.c_int tl_camera_set_camera_disconnect_callback(TL_CAMERA_DISCONNECT_CALLBACK handler, ctypes.c_void_p context)
    addfunc(lib, "tl_camera_set_camera_disconnect_callback", restype = ctypes.c_int,
            argtypes = [TL_CAMERA_DISCONNECT_CALLBACK, ctypes.c_void_p],
            argnames = ["handler", "context"] )
    #  ctypes.c_int tl_camera_open_sdk()
    addfunc(lib, "tl_camera_open_sdk", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int tl_camera_close_sdk()
    addfunc(lib, "tl_camera_close_sdk", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_char_p tl_camera_get_last_error()
    addfunc(lib, "tl_camera_get_last_error", restype = ctypes.c_char_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int tl_camera_discover_available_cameras(ctypes.c_char_p serial_numbers, ctypes.c_int str_length)
    addfunc(lib, "tl_camera_discover_available_cameras", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.c_int],
            argnames = ["serial_numbers", "str_length"] )
    #  ctypes.c_int _internal_command(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p data, ctypes.c_char_p response, ctypes.c_int response_size)
    addfunc(lib, "_internal_command", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "data", "response", "response_size"] )
    #  ctypes.c_int tl_camera_get_exposure_time(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_longlong) exposure_time_us)
    addfunc(lib, "tl_camera_get_exposure_time", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_longlong)],
            argnames = ["tl_camera_handle", "exposure_time_us"] )
    #  ctypes.c_int tl_camera_set_exposure_time(ctypes.c_void_p tl_camera_handle, ctypes.c_longlong exposure_time_us)
    addfunc(lib, "tl_camera_set_exposure_time", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_longlong],
            argnames = ["tl_camera_handle", "exposure_time_us"] )
    #  ctypes.c_int tl_camera_get_exposure_time_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_longlong) exposure_time_us_min, ctypes.POINTER(ctypes.c_longlong) exposure_time_us_max)
    addfunc(lib, "tl_camera_get_exposure_time_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_longlong), ctypes.POINTER(ctypes.c_longlong)],
            argnames = ["tl_camera_handle", "exposure_time_us_min", "exposure_time_us_max"] )
    #  ctypes.c_int tl_camera_get_image_poll_timeout(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) timeout_ms)
    addfunc(lib, "tl_camera_get_image_poll_timeout", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "timeout_ms"] )
    #  ctypes.c_int tl_camera_set_image_poll_timeout(ctypes.c_void_p tl_camera_handle, ctypes.c_int timeout_ms)
    addfunc(lib, "tl_camera_set_image_poll_timeout", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "timeout_ms"] )
    #  ctypes.c_int tl_camera_get_pending_frame_or_null(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.POINTER(ctypes.c_ushort)) image_buffer, ctypes.POINTER(ctypes.c_int) frame_count, ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte)) metadata, ctypes.POINTER(ctypes.c_int) metadata_size_in_bytes)
    addfunc(lib, "tl_camera_get_pending_frame_or_null", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_ushort)), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte)), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "image_buffer", "frame_count", "metadata", "metadata_size_in_bytes"] )
    #  ctypes.c_int tl_camera_get_firmware_version(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p firmware_version, ctypes.c_int str_length)
    addfunc(lib, "tl_camera_get_firmware_version", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "firmware_version", "str_length"] )
    #  ctypes.c_int tl_camera_get_frame_time(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) frame_time_us)
    addfunc(lib, "tl_camera_get_frame_time", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "frame_time_us"] )
    #  ctypes.c_int tl_camera_get_measured_frame_rate(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) frames_per_second)
    addfunc(lib, "tl_camera_get_measured_frame_rate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)],
            argnames = ["tl_camera_handle", "frames_per_second"] )
    #  ctypes.c_int tl_camera_get_trigger_polarity(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) trigger_polarity_enum)
    addfunc(lib, "tl_camera_get_trigger_polarity", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "trigger_polarity_enum"] )
    #  ctypes.c_int tl_camera_set_trigger_polarity(ctypes.c_void_p tl_camera_handle, ctypes.c_int trigger_polarity_enum)
    addfunc(lib, "tl_camera_set_trigger_polarity", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "trigger_polarity_enum"] )
    #  ctypes.c_int tl_camera_get_binx(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) binx)
    addfunc(lib, "tl_camera_get_binx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "binx"] )
    #  ctypes.c_int tl_camera_set_binx(ctypes.c_void_p tl_camera_handle, ctypes.c_int binx)
    addfunc(lib, "tl_camera_set_binx", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "binx"] )
    #  ctypes.c_int tl_camera_get_sensor_readout_time(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) sensor_readout_time_ns)
    addfunc(lib, "tl_camera_get_sensor_readout_time", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "sensor_readout_time_ns"] )
    #  ctypes.c_int tl_camera_get_binx_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) hbin_min, ctypes.POINTER(ctypes.c_int) hbin_max)
    addfunc(lib, "tl_camera_get_binx_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "hbin_min", "hbin_max"] )
    #  ctypes.c_int tl_camera_get_is_hot_pixel_correction_enabled(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_hot_pixel_correction_enabled)
    addfunc(lib, "tl_camera_get_is_hot_pixel_correction_enabled", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_hot_pixel_correction_enabled"] )
    #  ctypes.c_int tl_camera_set_is_hot_pixel_correction_enabled(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_hot_pixel_correction_enabled)
    addfunc(lib, "tl_camera_set_is_hot_pixel_correction_enabled", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "is_hot_pixel_correction_enabled"] )
    #  ctypes.c_int tl_camera_get_hot_pixel_correction_threshold(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) hot_pixel_correction_threshold)
    addfunc(lib, "tl_camera_get_hot_pixel_correction_threshold", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "hot_pixel_correction_threshold"] )
    #  ctypes.c_int tl_camera_set_hot_pixel_correction_threshold(ctypes.c_void_p tl_camera_handle, ctypes.c_int hot_pixel_correction_threshold)
    addfunc(lib, "tl_camera_set_hot_pixel_correction_threshold", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "hot_pixel_correction_threshold"] )
    #  ctypes.c_int tl_camera_get_hot_pixel_correction_threshold_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) hot_pixel_correction_threshold_min, ctypes.POINTER(ctypes.c_int) hot_pixel_correction_threshold_max)
    addfunc(lib, "tl_camera_get_hot_pixel_correction_threshold_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "hot_pixel_correction_threshold_min", "hot_pixel_correction_threshold_max"] )
    #  ctypes.c_int tl_camera_get_image_width(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) width_pixels)
    addfunc(lib, "tl_camera_get_image_width", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "width_pixels"] )
    #  ctypes.c_int tl_camera_get_image_height(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) height_pixels)
    addfunc(lib, "tl_camera_get_image_height", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "height_pixels"] )
    #  ctypes.c_int tl_camera_get_sensor_width(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) width_pixels)
    addfunc(lib, "tl_camera_get_sensor_width", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "width_pixels"] )
    #  ctypes.c_int tl_camera_get_sensor_height(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) height_pixels)
    addfunc(lib, "tl_camera_get_sensor_height", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "height_pixels"] )
    #  ctypes.c_int tl_camera_get_gain_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) gain_min, ctypes.POINTER(ctypes.c_int) gain_max)
    addfunc(lib, "tl_camera_get_gain_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "gain_min", "gain_max"] )
    #  ctypes.c_int tl_camera_get_image_width_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) image_width_pixels_min, ctypes.POINTER(ctypes.c_int) image_width_pixels_max)
    addfunc(lib, "tl_camera_get_image_width_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "image_width_pixels_min", "image_width_pixels_max"] )
    #  ctypes.c_int tl_camera_get_image_height_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) image_height_pixels_min, ctypes.POINTER(ctypes.c_int) image_height_pixels_max)
    addfunc(lib, "tl_camera_get_image_height_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "image_height_pixels_min", "image_height_pixels_max"] )
    #  ctypes.c_int tl_camera_get_model(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p model, ctypes.c_int str_length)
    addfunc(lib, "tl_camera_get_model", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "model", "str_length"] )
    #  ctypes.c_int tl_camera_get_model_string_length_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) model_min, ctypes.POINTER(ctypes.c_int) model_max)
    addfunc(lib, "tl_camera_get_model_string_length_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "model_min", "model_max"] )
    #  ctypes.c_int tl_camera_get_name(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p name, ctypes.c_int str_length)
    addfunc(lib, "tl_camera_get_name", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "name", "str_length"] )
    #  ctypes.c_int tl_camera_set_name(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p name)
    addfunc(lib, "tl_camera_set_name", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["tl_camera_handle", "name"] )
    #  ctypes.c_int tl_camera_get_name_string_length_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) name_min, ctypes.POINTER(ctypes.c_int) name_max)
    addfunc(lib, "tl_camera_get_name_string_length_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "name_min", "name_max"] )
    #  ctypes.c_int tl_camera_get_frames_per_trigger_zero_for_unlimited(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_uint) number_of_frames_per_trigger_or_zero_for_unlimited)
    addfunc(lib, "tl_camera_get_frames_per_trigger_zero_for_unlimited", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["tl_camera_handle", "number_of_frames_per_trigger_or_zero_for_unlimited"] )
    #  ctypes.c_int tl_camera_set_frames_per_trigger_zero_for_unlimited(ctypes.c_void_p tl_camera_handle, ctypes.c_uint number_of_frames_per_trigger_or_zero_for_unlimited)
    addfunc(lib, "tl_camera_set_frames_per_trigger_zero_for_unlimited", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["tl_camera_handle", "number_of_frames_per_trigger_or_zero_for_unlimited"] )
    #  ctypes.c_int tl_camera_get_frames_per_trigger_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_uint) number_of_frames_per_trigger_min, ctypes.POINTER(ctypes.c_uint) number_of_frames_per_trigger_max)
    addfunc(lib, "tl_camera_get_frames_per_trigger_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)],
            argnames = ["tl_camera_handle", "number_of_frames_per_trigger_min", "number_of_frames_per_trigger_max"] )
    #  ctypes.c_int tl_camera_get_usb_port_type(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) usb_port_type)
    addfunc(lib, "tl_camera_get_usb_port_type", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "usb_port_type"] )
    #  ctypes.c_int tl_camera_get_communication_interface(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) communication_interface)
    addfunc(lib, "tl_camera_get_communication_interface", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "communication_interface"] )
    #  ctypes.c_int tl_camera_get_is_data_rate_supported(ctypes.c_void_p tl_camera_handle, ctypes.c_int data_rate, ctypes.POINTER(ctypes.c_int) is_data_rate_supported)
    addfunc(lib, "tl_camera_get_is_data_rate_supported", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "data_rate", "is_data_rate_supported"] )
    #  ctypes.c_int tl_camera_get_is_operation_mode_supported(ctypes.c_void_p tl_camera_handle, ctypes.c_int operation_mode, ctypes.POINTER(ctypes.c_int) is_operation_mode_supported)
    addfunc(lib, "tl_camera_get_is_operation_mode_supported", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "operation_mode", "is_operation_mode_supported"] )
    #  ctypes.c_int tl_camera_get_is_armed(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_armed)
    addfunc(lib, "tl_camera_get_is_armed", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_armed"] )
    #  ctypes.c_int tl_camera_get_is_eep_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_eep_supported)
    addfunc(lib, "tl_camera_get_is_eep_supported", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_eep_supported"] )
    #  ctypes.c_int tl_camera_get_is_led_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_led_supported)
    addfunc(lib, "tl_camera_get_is_led_supported", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_led_supported"] )
    #  ctypes.c_int tl_camera_get_is_cooling_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_cooling_supported)
    addfunc(lib, "tl_camera_get_is_cooling_supported", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_cooling_supported"] )
    #  ctypes.c_int tl_camera_get_is_taps_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_taps_supported, ctypes.c_int tap)
    addfunc(lib, "tl_camera_get_is_taps_supported", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_int],
            argnames = ["tl_camera_handle", "is_taps_supported", "tap"] )
    #  ctypes.c_int tl_camera_get_is_nir_boost_supported(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_nir_boost_supported)
    addfunc(lib, "tl_camera_get_is_nir_boost_supported", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_nir_boost_supported"] )
    #  ctypes.c_int tl_camera_get_camera_color_correction_matrix_output_color_space(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p output_color_space)
    addfunc(lib, "tl_camera_get_camera_color_correction_matrix_output_color_space", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["tl_camera_handle", "output_color_space"] )
    #  ctypes.c_int tl_camera_get_camera_sensor_type(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) camera_sensor_type)
    addfunc(lib, "tl_camera_get_camera_sensor_type", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "camera_sensor_type"] )
    #  ctypes.c_int tl_camera_get_polar_phase(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) polar_phase)
    addfunc(lib, "tl_camera_get_polar_phase", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "polar_phase"] )
    #  ctypes.c_int tl_camera_get_taps(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) taps)
    addfunc(lib, "tl_camera_get_taps", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "taps"] )
    #  ctypes.c_int tl_camera_set_taps(ctypes.c_void_p tl_camera_handle, ctypes.c_int taps)
    addfunc(lib, "tl_camera_set_taps", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "taps"] )
    #  ctypes.c_int tl_camera_get_tap_balance_enable(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) taps_balance_enable)
    addfunc(lib, "tl_camera_get_tap_balance_enable", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "taps_balance_enable"] )
    #  ctypes.c_int tl_camera_set_tap_balance_enable(ctypes.c_void_p tl_camera_handle, ctypes.c_int taps_balance_enable)
    addfunc(lib, "tl_camera_set_tap_balance_enable", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "taps_balance_enable"] )
    #  ctypes.c_int tl_camera_get_nir_boost_enable(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) nir_boost_enable)
    addfunc(lib, "tl_camera_get_nir_boost_enable", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "nir_boost_enable"] )
    #  ctypes.c_int tl_camera_set_nir_boost_enable(ctypes.c_void_p tl_camera_handle, ctypes.c_int nir_boost_enable)
    addfunc(lib, "tl_camera_set_nir_boost_enable", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "nir_boost_enable"] )
    #  ctypes.c_int tl_camera_get_cooling_enable(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_cooling_enabled)
    addfunc(lib, "tl_camera_get_cooling_enable", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_cooling_enabled"] )
    #  ctypes.c_int tl_camera_set_cooling_enable(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_cooling_enabled)
    addfunc(lib, "tl_camera_set_cooling_enable", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "is_cooling_enabled"] )
    #  ctypes.c_int tl_camera_get_default_white_balance_matrix(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_float) matrix)
    addfunc(lib, "tl_camera_get_default_white_balance_matrix", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float)],
            argnames = ["tl_camera_handle", "matrix"] )
    #  ctypes.c_int tl_camera_get_operation_mode(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) operation_mode)
    addfunc(lib, "tl_camera_get_operation_mode", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "operation_mode"] )
    #  ctypes.c_int tl_camera_set_operation_mode(ctypes.c_void_p tl_camera_handle, ctypes.c_int operation_mode)
    addfunc(lib, "tl_camera_set_operation_mode", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "operation_mode"] )
    #  ctypes.c_int tl_camera_get_color_correction_matrix(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_float) matrix)
    addfunc(lib, "tl_camera_get_color_correction_matrix", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float)],
            argnames = ["tl_camera_handle", "matrix"] )
    #  ctypes.c_int tl_camera_get_color_filter_array_phase(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) cfaPhase)
    addfunc(lib, "tl_camera_get_color_filter_array_phase", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "cfaPhase"] )
    #  ctypes.c_int tl_camera_get_data_rate(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) data_rate)
    addfunc(lib, "tl_camera_get_data_rate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "data_rate"] )
    #  ctypes.c_int tl_camera_set_data_rate(ctypes.c_void_p tl_camera_handle, ctypes.c_int data_rate)
    addfunc(lib, "tl_camera_set_data_rate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "data_rate"] )
    #  ctypes.c_int tl_camera_get_sensor_pixel_size_bytes(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) sensor_pixel_size_bytes)
    addfunc(lib, "tl_camera_get_sensor_pixel_size_bytes", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "sensor_pixel_size_bytes"] )
    #  ctypes.c_int tl_camera_get_sensor_pixel_width(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) pixel_width_um)
    addfunc(lib, "tl_camera_get_sensor_pixel_width", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)],
            argnames = ["tl_camera_handle", "pixel_width_um"] )
    #  ctypes.c_int tl_camera_get_sensor_pixel_height(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) pixel_height_um)
    addfunc(lib, "tl_camera_get_sensor_pixel_height", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)],
            argnames = ["tl_camera_handle", "pixel_height_um"] )
    #  ctypes.c_int tl_camera_get_bit_depth(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) pixel_bit_depth)
    addfunc(lib, "tl_camera_get_bit_depth", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "pixel_bit_depth"] )
    #  ctypes.c_int tl_camera_get_roi(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) upper_left_x_pixels, ctypes.POINTER(ctypes.c_int) upper_left_y_pixels, ctypes.POINTER(ctypes.c_int) lower_right_x_pixels, ctypes.POINTER(ctypes.c_int) lower_right_y_pixels)
    addfunc(lib, "tl_camera_get_roi", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "upper_left_x_pixels", "upper_left_y_pixels", "lower_right_x_pixels", "lower_right_y_pixels"] )
    #  ctypes.c_int tl_camera_set_roi(ctypes.c_void_p tl_camera_handle, ctypes.c_int upper_left_x_pixels, ctypes.c_int upper_left_y_pixels, ctypes.c_int lower_right_x_pixels, ctypes.c_int lower_right_y_pixels)
    addfunc(lib, "tl_camera_set_roi", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["tl_camera_handle", "upper_left_x_pixels", "upper_left_y_pixels", "lower_right_x_pixels", "lower_right_y_pixels"] )
    #  ctypes.c_int tl_camera_get_roi_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) upper_left_x_pixels_min, ctypes.POINTER(ctypes.c_int) upper_left_y_pixels_min, ctypes.POINTER(ctypes.c_int) lower_right_x_pixels_min, ctypes.POINTER(ctypes.c_int) lower_right_y_pixels_min, ctypes.POINTER(ctypes.c_int) upper_left_x_pixels_max, ctypes.POINTER(ctypes.c_int) upper_left_y_pixels_max, ctypes.POINTER(ctypes.c_int) lower_right_x_pixels_max, ctypes.POINTER(ctypes.c_int) lower_right_y_pixels_max)
    addfunc(lib, "tl_camera_get_roi_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "upper_left_x_pixels_min", "upper_left_y_pixels_min", "lower_right_x_pixels_min", "lower_right_y_pixels_min", "upper_left_x_pixels_max", "upper_left_y_pixels_max", "lower_right_x_pixels_max", "lower_right_y_pixels_max"] )
    #  ctypes.c_int tl_camera_get_serial_number(ctypes.c_void_p tl_camera_handle, ctypes.c_char_p serial_number, ctypes.c_int str_length)
    addfunc(lib, "tl_camera_get_serial_number", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "serial_number", "str_length"] )
    #  ctypes.c_int tl_camera_get_serial_number_string_length_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) serial_number_min, ctypes.POINTER(ctypes.c_int) serial_number_max)
    addfunc(lib, "tl_camera_get_serial_number_string_length_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "serial_number_min", "serial_number_max"] )
    #  ctypes.c_int tl_camera_get_is_led_on(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_led_on)
    addfunc(lib, "tl_camera_get_is_led_on", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_led_on"] )
    #  ctypes.c_int tl_camera_set_is_led_on(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_led_on)
    addfunc(lib, "tl_camera_set_is_led_on", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "is_led_on"] )
    #  ctypes.c_int tl_camera_get_eep_status(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) eep_status_enum)
    addfunc(lib, "tl_camera_get_eep_status", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "eep_status_enum"] )
    #  ctypes.c_int tl_camera_set_is_eep_enabled(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_eep_enabled)
    addfunc(lib, "tl_camera_set_is_eep_enabled", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "is_eep_enabled"] )
    #  ctypes.c_int tl_camera_get_biny(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) biny)
    addfunc(lib, "tl_camera_get_biny", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "biny"] )
    #  ctypes.c_int tl_camera_set_biny(ctypes.c_void_p tl_camera_handle, ctypes.c_int biny)
    addfunc(lib, "tl_camera_set_biny", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "biny"] )
    #  ctypes.c_int tl_camera_get_gain(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) gain)
    addfunc(lib, "tl_camera_get_gain", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "gain"] )
    #  ctypes.c_int tl_camera_set_gain(ctypes.c_void_p tl_camera_handle, ctypes.c_int gain)
    addfunc(lib, "tl_camera_set_gain", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "gain"] )
    #  ctypes.c_int tl_camera_get_black_level(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) black_level)
    addfunc(lib, "tl_camera_get_black_level", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "black_level"] )
    #  ctypes.c_int tl_camera_set_black_level(ctypes.c_void_p tl_camera_handle, ctypes.c_int black_level)
    addfunc(lib, "tl_camera_set_black_level", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "black_level"] )
    #  ctypes.c_int tl_camera_get_black_level_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) min, ctypes.POINTER(ctypes.c_int) max)
    addfunc(lib, "tl_camera_get_black_level_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "min", "max"] )
    #  ctypes.c_int tl_camera_get_biny_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) vbin_min, ctypes.POINTER(ctypes.c_int) vbin_max)
    addfunc(lib, "tl_camera_get_biny_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "vbin_min", "vbin_max"] )
    #  ctypes.c_int tl_camera_open_camera(ctypes.c_char_p camera_serial_number, ctypes.POINTER(ctypes.c_void_p) tl_camera_handle)
    addfunc(lib, "tl_camera_open_camera", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["camera_serial_number", "tl_camera_handle"] )
    #  ctypes.c_int tl_camera_close_camera(ctypes.c_void_p tl_camera_handle)
    addfunc(lib, "tl_camera_close_camera", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["tl_camera_handle"] )
    #  ctypes.c_int tl_camera_arm(ctypes.c_void_p tl_camera_handle, ctypes.c_int number_of_frames_to_buffer)
    addfunc(lib, "tl_camera_arm", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "number_of_frames_to_buffer"] )
    #  ctypes.c_int tl_camera_issue_software_trigger(ctypes.c_void_p tl_camera_handle)
    addfunc(lib, "tl_camera_issue_software_trigger", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["tl_camera_handle"] )
    #  ctypes.c_int tl_camera_disarm(ctypes.c_void_p tl_camera_handle)
    addfunc(lib, "tl_camera_disarm", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["tl_camera_handle"] )
    #  ctypes.c_int tl_camera_get_timestamp_clock_frequency(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) timestamp_clock_frequency_hz_or_zero)
    addfunc(lib, "tl_camera_get_timestamp_clock_frequency", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "timestamp_clock_frequency_hz_or_zero"] )
    #  ctypes.c_int tl_camera_get_frame_rate_control_value_range(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) frame_rate_fps_min, ctypes.POINTER(ctypes.c_double) frame_rate_fps_max)
    addfunc(lib, "tl_camera_get_frame_rate_control_value_range", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)],
            argnames = ["tl_camera_handle", "frame_rate_fps_min", "frame_rate_fps_max"] )
    #  ctypes.c_int tl_camera_get_is_frame_rate_control_enabled(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_int) is_enabled)
    addfunc(lib, "tl_camera_get_is_frame_rate_control_enabled", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "is_enabled"] )
    #  ctypes.c_int tl_camera_set_frame_rate_control_value(ctypes.c_void_p tl_camera_handle, ctypes.c_double frame_rate_fps)
    addfunc(lib, "tl_camera_set_frame_rate_control_value", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_double],
            argnames = ["tl_camera_handle", "frame_rate_fps"] )
    #  ctypes.c_int tl_camera_set_is_frame_rate_control_enabled(ctypes.c_void_p tl_camera_handle, ctypes.c_int is_enabled)
    addfunc(lib, "tl_camera_set_is_frame_rate_control_enabled", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["tl_camera_handle", "is_enabled"] )
    #  ctypes.c_int tl_camera_get_frame_rate_control_value(ctypes.c_void_p tl_camera_handle, ctypes.POINTER(ctypes.c_double) frame_rate_fps)
    addfunc(lib, "tl_camera_get_frame_rate_control_value", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)],
            argnames = ["tl_camera_handle", "frame_rate_fps"] )
    #  ctypes.c_int tl_camera_convert_gain_to_decibels(ctypes.c_void_p tl_camera_handle, ctypes.c_int index_of_gain_value, ctypes.POINTER(ctypes.c_double) gain_dB)
    addfunc(lib, "tl_camera_convert_gain_to_decibels", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double)],
            argnames = ["tl_camera_handle", "index_of_gain_value", "gain_dB"] )
    #  ctypes.c_int tl_camera_convert_decibels_to_gain(ctypes.c_void_p tl_camera_handle, ctypes.c_double gain_dB, ctypes.POINTER(ctypes.c_int) index_of_gain_value)
    addfunc(lib, "tl_camera_convert_decibels_to_gain", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.POINTER(ctypes.c_int)],
            argnames = ["tl_camera_handle", "gain_dB", "index_of_gain_value"] )


