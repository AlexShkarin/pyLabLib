# pylint: disable=wrong-spelling-in-comment

from .base import SmarActError
from ...core.utils import ctypes_wrap, py3
from .SmarActControl_defs import drSA_CTL_ERROR, SA_CTL_ERROR, SA_CTL_PKEY
from .SmarActControl_defs import define_functions

from ..utils import load_lib

import ctypes
import os
import platform



class SmarActControlLibError(SmarActError):
    """Generic SmarActControl library error"""
    def __init__(self, func, arguments, code, lib=None):
        self.func=func
        self.arguments=arguments
        self.code=code
        self.name=drSA_CTL_ERROR.get(code,"UNKNOWN")
        self.desc=py3.as_str(lib.SA_CTL_GetResultInfo(code)) if lib is not None else ""
        self.msg="function '{}' returned an error {}({}): {}".format(func,self.code,self.name,self.desc)
        super().__init__(self.msg)
def errcheck(passing=None, lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of Andor Shamrock library functions.
    `passing` is a list specifying which return codes are acceptable (by default only 0, which is success code, is acceptable).
    """
    passing=set(passing) if passing is not None else set()
    passing.add(SA_CTL_ERROR.SA_CTL_ERROR_NONE) # always allow success
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result not in passing:
            raise SmarActControlLibError(func.__name__,arguments,result,lib=lib)
        return result
    return errchecker



keyprops = {
    SA_CTL_PKEY.SA_CTL_PKEY_NUMBER_OF_CHANNELS                     : ("number_of_channels"               , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_NUMBER_OF_BUS_MODULES                  : ("number_of_bus_modules"            , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_DEVICE_STATE                           : ("device_state"                     , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_DEVICE_SERIAL_NUMBER                   : ("device_serial_number"             , "dev", "str"),
    SA_CTL_PKEY.SA_CTL_PKEY_DEVICE_NAME                            : ("device_name"                      , "dev", "str"),
    SA_CTL_PKEY.SA_CTL_PKEY_EMERGENCY_STOP_MODE                    : ("emergency_stop_mode"              , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_NETWORK_DISCOVER_MODE                  : ("network_discover_mode"            , "dev", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_POWER_SUPPLY_ENABLED                   : ("power_supply_enabled"             , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_MODULE_STATE                           : ("module_state"                     , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_NUMBER_OF_BUS_MODULE_CHANNELS          : ("number_of_bus_module_channels"    , "mod", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_AMPLIFIER_ENABLED                      : ("amplifier_enabled"                , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POSITIONER_CONTROL_OPTIONS             : ("positioner_control_options"       , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_ACTUATOR_MODE                          : ("actuator_mode"                    , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_CONTROL_LOOP_INPUT                     : ("control_loop_input"               , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_SENSOR_INPUT_SELECT                    : ("sensor_input_select"              , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POSITIONER_TYPE                        : ("positioner_type"                  , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POSITIONER_TYPE_NAME                   : ("positioner_type_name"             , "cha", "str"),
    SA_CTL_PKEY.SA_CTL_PKEY_MOVE_MODE                              : ("move_mode"                        , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_CHANNEL_STATE                          : ("channel_state"                    , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POSITION                               : ("position"                         , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_TARGET_POSITION                        : ("target_position"                  , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_SCAN_POSITION                          : ("scan_position"                    , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_SCAN_VELOCITY                          : ("scan_velocity"                    , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_HOLD_TIME                              : ("hold_time"                        , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_MOVE_VELOCITY                          : ("move_velocity"                    , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_MOVE_ACCELERATION                      : ("move_acceleration"                , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_MAX_CL_FREQUENCY                       : ("max_cl_frequency"                 , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_DEFAULT_MAX_CL_FREQUENCY               : ("default_max_cl_frequency"         , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_STEP_FREQUENCY                         : ("step_frequency"                   , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_STEP_AMPLITUDE                         : ("step_amplitude"                   , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_FOLLOWING_ERROR_LIMIT                  : ("following_error_limit"            , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_FOLLOWING_ERROR                        : ("following_error"                  , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_BROADCAST_STOP_OPTIONS                 : ("broadcast_stop_options"           , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_SENSOR_POWER_MODE                      : ("sensor_power_mode"                , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_SENSOR_POWER_SAVE_DELAY                : ("sensor_power_save_delay"          , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POSITION_MEAN_SHIFT                    : ("position_mean_shift"              , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_SAFE_DIRECTION                         : ("safe_direction"                   , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_CL_INPUT_SENSOR_VALUE                  : ("cl_input_sensor_value"            , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_CL_INPUT_AUX_VALUE                     : ("cl_input_aux_value"               , "cha", "i64"),

    SA_CTL_PKEY.SA_CTL_PKEY_LOGICAL_SCALE_OFFSET                   : ("logical_scale_offset"             , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_LOGICAL_SCALE_INVERSION                : ("logical_scale_inversion"          , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_RANGE_LIMIT_MIN                        : ("range_limit_min"                  , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_RANGE_LIMIT_MAX                        : ("range_limit_max"                  , "cha", "i64"),

    SA_CTL_PKEY.SA_CTL_PKEY_CALIBRATION_OPTIONS                    : ("calibration_options"              , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_SIGNAL_CORRECTION_OPTIONS              : ("signal_correction_options"        , "cha", "i32"),
    
    SA_CTL_PKEY.SA_CTL_PKEY_REFERENCING_OPTIONS                    : ("referencing_options"              , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_DISTANCE_TO_REF_MARK                   : ("distance_to_ref_mark"             , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_DIST_CODE_INVERTED                     : ("dist_code_inverted"               , "cha", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_POS_MOVEMENT_TYPE                      : ("pos_movement_type"                , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_IS_CUSTOM_TYPE                     : ("pos_is_custom_type"               , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_BASE_UNIT                          : ("pos_base_unit"                    , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_BASE_RESOLUTION                    : ("pos_base_resolution"              , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_P_GAIN                             : ("pos_p_gain"                       , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_I_GAIN                             : ("pos_i_gain"                       , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_D_GAIN                             : ("pos_d_gain"                       , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_PID_SHIFT                          : ("pos_pid_shift"                    , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_ANTI_WINDUP                        : ("pos_anti_windup"                  , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_ESD_DIST_TH                        : ("pos_esd_dist_th"                  , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_ESD_COUNTER_TH                     : ("pos_esd_counter_th"               , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_TARGET_REACHED_TH                  : ("pos_target_reached_th"            , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_SAVE                               : ("pos_save"                         , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_POS_WRITE_PROTECTION                   : ("pos_write_protection"             , "cha", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_STREAM_BASE_RATE                       : ("stream_base_rate"                 , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_STREAM_EXT_SYNC_RATE                   : ("stream_ext_sync_rate"             , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_STREAM_OPTIONS                         : ("stream_options"                   , "dev", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_CHANNEL_ERROR                          : ("channel_error"                    , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_CHANNEL_TEMPERATURE                    : ("channel_temperature"              , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_BUS_MODULE_TEMPERATURE                 : ("bus_module_temperature"           , "mod", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_AUX_POSITIONER_TYPE                    : ("aux_positioner_type"              , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_POSITIONER_TYPE_NAME               : ("aux_positioner_type_name"         , "cha", "str"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_INPUT_SELECT                       : ("aux_input_select"                 , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_IO_MODULE_INPUT_INDEX              : ("aux_io_module_input_index"        , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_DIRECTION_INVERSION                : ("aux_direction_inversion"          , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_IO_MODULE_INPUT0_VALUE             : ("aux_io_module_input0_value"       , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_IO_MODULE_INPUT1_VALUE             : ("aux_io_module_input1_value"       , "cha", "i64"),
    # SA_CTL_PKEY.SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT0_VALUE         : ("aux_sensor_module_input0_value"   , "cha", "i64"),
    # SA_CTL_PKEY.SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT1_VALUE         : ("aux_sensor_module_input1_value"   , "cha", "i64"),
    # SA_CTL_PKEY.SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT_INDEX          : ("aux_sensor_module_input_index"    , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_DIGITAL_INPUT_VALUE                : ("aux_digital_input_value"          , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_VALUE               : ("aux_digital_output_value"         , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_SET                 : ("aux_digital_output_set"           , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_CLEAR               : ("aux_digital_output_clear"         , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_ANALOG_OUTPUT_VALUE0               : ("aux_analog_output_value0"         , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUX_ANALOG_OUTPUT_VALUE1               : ("aux_analog_output_value1"         , "mod", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_IO_MODULE_OPTIONS                      : ("io_module_options"                , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_IO_MODULE_VOLTAGE                      : ("io_module_voltage"                , "mod", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_IO_MODULE_ANALOG_INPUT_RANGE           : ("io_module_analog_input_range"     , "mod", "i32"),

    # SA_CTL_PKEY.SA_CTL_PKEY_THD_INPUT_SELECT                       : ("thd_input_select"                 , "dev", "i32"),
    # SA_CTL_PKEY.SA_CTL_PKEY_THD_IO_MODULE_INPUT_INDEX              : ("thd_io_module_input_index"        , "dev", "i32"),
    # SA_CTL_PKEY.SA_CTL_PKEY_THD_SENSOR_MODULE_INPUT_INDEX          : ("thd_sensor_module_input_index"    , "dev", "i32"),
    # SA_CTL_PKEY.SA_CTL_PKEY_THD_THRESHOLD_HIGH                     : ("thd_threshold_high"               , "dev", "i32"),
    # SA_CTL_PKEY.SA_CTL_PKEY_THD_THRESHOLD_LOW                      : ("thd_threshold_low"                , "dev", "i32"),
    # SA_CTL_PKEY.SA_CTL_PKEY_THD_INVERSION                          : ("thd_inversion"                    , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_DEV_INPUT_TRIG_MODE                    : ("dev_input_trig_mode"              , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_DEV_INPUT_TRIG_CONDITION               : ("dev_input_trig_condition"         , "dev", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_CH_OUTPUT_TRIG_MODE                    : ("ch_output_trig_mode"              , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_CH_OUTPUT_TRIG_POLARITY                : ("ch_output_trig_polarity"          , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_CH_OUTPUT_TRIG_PULSE_WIDTH             : ("ch_output_trig_pulse_width"       , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_CH_POS_COMP_START_THRESHOLD            : ("ch_pos_comp_start_threshold"      , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_CH_POS_COMP_INCREMENT                  : ("ch_pos_comp_increment"            , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_CH_POS_COMP_DIRECTION                  : ("ch_pos_comp_direction"            , "cha", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_CH_POS_COMP_LIMIT_MIN                  : ("ch_pos_comp_limit_min"            , "cha", "i64"),
    SA_CTL_PKEY.SA_CTL_PKEY_CH_POS_COMP_LIMIT_MAX                  : ("ch_pos_comp_limit_max"            , "cha", "i64"),

    # SA_CTL_PKEY.SA_CTL_PKEY_HM_STATE                               : ("hm_state"                         , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_HM_LOCK_OPTIONS                        : ("hm_lock_options"                  , "dev", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_HM_DEFAULT_LOCK_OPTIONS                : ("hm_default_lock_options"          , "dev", "i32"),

    SA_CTL_PKEY.SA_CTL_PKEY_EVENT_NOTIFICATION_OPTIONS             : ("event_notification_options"       , "api", "i32"),
    SA_CTL_PKEY.SA_CTL_PKEY_AUTO_RECONNECT                         : ("auto_reconnect"                   , "api", "i32"),
}
nameprops={n:(i,t,k) for i,(n,t,k) in keyprops.items()}


class SmarActControlLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is supplied together with the controller\n"+load_lib.par_error_message.format("smaract_mcs2")
        sdk_folders=[load_lib.get_environ_folder("MCS2_SDK"),os.path.join("C:","SmarAct","MCS2","SDK")]
        sdk_folders=[f for f in sdk_folders if f is not None]
        archbit=platform.architecture()[0][:2]
        folders=[os.path.join(f,"lib{}".format("" if archbit=="32" else archbit)) for f in sdk_folders]
        self.lib=load_lib.load_lib("SmarActCTL.dll",locations=("parameter/smaract_mcs2",)+tuple(folders)+("global",),error_message=error_message,call_conv="cdecl")
        lib=self.lib
        define_functions(lib)

        rwrapper=ctypes_wrap.CFunctionWrapper(default_rvals="pointer",pointer_byref=True)
        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib=self),default_rvals="pointer",pointer_byref=True)

        devlist_strlen=2**14
        devlist_strprep=ctypes_wrap.strprep(devlist_strlen)
        prop_strlen=2**8
        prop_strprep=ctypes_wrap.strprep(prop_strlen)
        
        #  ctypes.c_char_p SA_CTL_GetFullVersionString()
        self.SA_CTL_GetFullVersionString=rwrapper(lib.SA_CTL_GetFullVersionString)
        #  ctypes.c_char_p SA_CTL_GetResultInfo(SA_CTL_Result_t result)
        self.SA_CTL_GetResultInfo=rwrapper(lib.SA_CTL_GetResultInfo)
        #  SA_CTL_Result_t SA_CTL_FindDevices(ctypes.c_char_p options, ctypes.c_char_p deviceList, ctypes.POINTER(ctypes.c_size_t) deviceListLen)
        self.SA_CTL_FindDevices=wrapper(lib.SA_CTL_FindDevices, args=["options"], rvals=["deviceList"],
            argprep={"deviceListLen":devlist_strlen,"deviceList":devlist_strprep}, byref=["deviceListLen"])
        
        #  SA_CTL_Result_t SA_CTL_Open(ctypes.POINTER(SA_CTL_DeviceHandle_t) dHandle, ctypes.c_char_p locator, ctypes.c_char_p config)
        self.SA_CTL_Open=wrapper(lib.SA_CTL_Open)
        #  SA_CTL_Result_t SA_CTL_Close(SA_CTL_DeviceHandle_t dHandle)
        self.SA_CTL_Close=wrapper(lib.SA_CTL_Close)
        #  SA_CTL_Result_t SA_CTL_Cancel(SA_CTL_DeviceHandle_t dHandle)
        self.SA_CTL_Cancel=wrapper(lib.SA_CTL_Cancel)

        #  SA_CTL_Result_t SA_CTL_GetProperty_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int32) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
        self.SA_CTL_GetProperty_i32_lib=wrapper(lib.SA_CTL_GetProperty_i32, args="all", rvals=["ioArraySize"])
        #  SA_CTL_Result_t SA_CTL_GetProperty_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int32) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
        self.SA_CTL_GetProperty_i32=wrapper(lib.SA_CTL_GetProperty_i32, args=["dHandle","idx","pkey"], rvals=["value"],
            argprep={"ioArraySize":1}, byref=["ioArraySize","value"])
        #  SA_CTL_Result_t SA_CTL_SetProperty_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_int32 value)
        self.SA_CTL_SetProperty_i32=wrapper(lib.SA_CTL_SetProperty_i32)
        #  SA_CTL_Result_t SA_CTL_SetPropertyArray_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int32) values, ctypes.c_size_t arraySize)
        self.SA_CTL_SetPropertyArray_i32=wrapper(lib.SA_CTL_SetPropertyArray_i32, rvals=[], args=["dHandle","idx","pkey","values"],
            argprep={"arraySize":lambda values:len(values)})  # pylint: disable=unnecessary-lambda
        #  SA_CTL_Result_t SA_CTL_GetProperty_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int64) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
        self.SA_CTL_GetProperty_i64_lib=wrapper(lib.SA_CTL_GetProperty_i64, args="all", rvals=["ioArraySize"])
        #  SA_CTL_Result_t SA_CTL_GetProperty_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int64) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
        self.SA_CTL_GetProperty_i64=wrapper(lib.SA_CTL_GetProperty_i64, args=["dHandle","idx","pkey"], rvals=["value"],
            argprep={"ioArraySize":1}, byref=["ioArraySize","value"])
        #  SA_CTL_Result_t SA_CTL_SetProperty_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_int64 value)
        self.SA_CTL_SetProperty_i64=wrapper(lib.SA_CTL_SetProperty_i64)
        #  SA_CTL_Result_t SA_CTL_SetPropertyArray_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int64) values, ctypes.c_size_t arraySize)
        self.SA_CTL_SetPropertyArray_i64=wrapper(lib.SA_CTL_SetPropertyArray_i64, args=["dHandle","idx","pkey","values"],
            argprep={"arraySize":lambda values:len(values)})  # pylint: disable=unnecessary-lambda
        #  SA_CTL_Result_t SA_CTL_GetProperty_s(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_char_p value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
        self.SA_CTL_GetProperty_s=wrapper(lib.SA_CTL_GetProperty_s, args=["dHandle","idx","pkey"], rvals=["value"],
            argprep={"value":prop_strprep,"ioArraySize":prop_strlen}, byref=["ioArraySize"])
        #  SA_CTL_Result_t SA_CTL_SetProperty_s(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_char_p value)
        self.SA_CTL_SetProperty_s=wrapper(lib.SA_CTL_SetProperty_s)

        #  SA_CTL_Result_t SA_CTL_CreateOutputBuffer(SA_CTL_DeviceHandle_t dHandle, ctypes.POINTER(SA_CTL_TransmitHandle_t) tHandle)
        self.SA_CTL_CreateOutputBuffer=wrapper(lib.SA_CTL_CreateOutputBuffer)
        #  SA_CTL_Result_t SA_CTL_FlushOutputBuffer(SA_CTL_DeviceHandle_t dHandle, SA_CTL_TransmitHandle_t tHandle)
        self.SA_CTL_FlushOutputBuffer=wrapper(lib.SA_CTL_FlushOutputBuffer)
        #  SA_CTL_Result_t SA_CTL_CancelOutputBuffer(SA_CTL_DeviceHandle_t dHandle, SA_CTL_TransmitHandle_t tHandle)
        self.SA_CTL_CancelOutputBuffer=wrapper(lib.SA_CTL_CancelOutputBuffer)
        #  SA_CTL_Result_t SA_CTL_OpenCommandGroup(SA_CTL_DeviceHandle_t dHandle, ctypes.POINTER(SA_CTL_TransmitHandle_t) tHandle, ctypes.c_uint32 triggerMode)
        self.SA_CTL_OpenCommandGroup=wrapper(lib.SA_CTL_OpenCommandGroup)
        #  SA_CTL_Result_t SA_CTL_CloseCommandGroup(SA_CTL_DeviceHandle_t dHandle, SA_CTL_TransmitHandle_t tHandle)
        self.SA_CTL_CloseCommandGroup=wrapper(lib.SA_CTL_CloseCommandGroup)
        #  SA_CTL_Result_t SA_CTL_CancelCommandGroup(SA_CTL_DeviceHandle_t dHandle, SA_CTL_TransmitHandle_t tHandle)
        self.SA_CTL_CancelCommandGroup=wrapper(lib.SA_CTL_CancelCommandGroup)
        
        #  SA_CTL_Result_t SA_CTL_WaitForEvent(SA_CTL_DeviceHandle_t dHandle, ctypes.POINTER(SA_CTL_Event_t) event, ctypes.c_uint32 timeout)
        self.SA_CTL_WaitForEvent=wrapper(lib.SA_CTL_WaitForEvent)
        #  ctypes.c_char_p SA_CTL_GetEventInfo(ctypes.POINTER(SA_CTL_Event_t) event)
        self.SA_CTL_GetEventInfo=rwrapper(lib.SA_CTL_GetEventInfo, rvals=[], byref=["event"])

        #  SA_CTL_Result_t SA_CTL_Calibrate(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_TransmitHandle_t tHandle)
        self.SA_CTL_Calibrate=wrapper(lib.SA_CTL_Calibrate)
        #  SA_CTL_Result_t SA_CTL_Reference(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_TransmitHandle_t tHandle)
        self.SA_CTL_Reference=wrapper(lib.SA_CTL_Reference)
        #  SA_CTL_Result_t SA_CTL_Move(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, ctypes.c_int64 moveValue, SA_CTL_TransmitHandle_t tHandle)
        self.SA_CTL_Move=wrapper(lib.SA_CTL_Move)
        #  SA_CTL_Result_t SA_CTL_Stop(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_TransmitHandle_t tHandle)
        self.SA_CTL_Stop=wrapper(lib.SA_CTL_Stop)

        # #  SA_CTL_Result_t SA_CTL_OpenStream(SA_CTL_DeviceHandle_t dHandle, ctypes.POINTER(SA_CTL_StreamHandle_t) sHandle, ctypes.c_uint32 triggerMode)
        # self.SA_CTL_OpenStream=wrapper(lib.SA_CTL_OpenStream)
        # #  SA_CTL_Result_t SA_CTL_StreamFrame(SA_CTL_DeviceHandle_t dHandle, SA_CTL_StreamHandle_t sHandle, ctypes.POINTER(ctypes.c_uint8) frameData, ctypes.c_uint32 frameSize)
        # self.SA_CTL_StreamFrame=wrapper(lib.SA_CTL_StreamFrame)
        # #  SA_CTL_Result_t SA_CTL_CloseStream(SA_CTL_DeviceHandle_t dHandle, SA_CTL_StreamHandle_t sHandle)
        # self.SA_CTL_CloseStream=wrapper(lib.SA_CTL_CloseStream)
        # #  SA_CTL_Result_t SA_CTL_AbortStream(SA_CTL_DeviceHandle_t dHandle, SA_CTL_StreamHandle_t sHandle)
        # self.SA_CTL_AbortStream=wrapper(lib.SA_CTL_AbortStream)

        # #  SA_CTL_Result_t SA_CTL_RequestReadProperty(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
        # self.SA_CTL_RequestReadProperty=wrapper(lib.SA_CTL_RequestReadProperty)
        # #  SA_CTL_Result_t SA_CTL_ReadProperty_i32(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID, ctypes.POINTER(ctypes.c_int32) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
        # self.SA_CTL_ReadProperty_i32=wrapper(lib.SA_CTL_ReadProperty_i32)
        # #  SA_CTL_Result_t SA_CTL_ReadProperty_i64(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID, ctypes.POINTER(ctypes.c_int64) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
        # self.SA_CTL_ReadProperty_i64=wrapper(lib.SA_CTL_ReadProperty_i64)
        # #  SA_CTL_Result_t SA_CTL_ReadProperty_s(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID, ctypes.c_char_p value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
        # self.SA_CTL_ReadProperty_s=wrapper(lib.SA_CTL_ReadProperty_s)
        # #  SA_CTL_Result_t SA_CTL_RequestWriteProperty_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_int32 value, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
        # self.SA_CTL_RequestWriteProperty_i32=wrapper(lib.SA_CTL_RequestWriteProperty_i32)
        # #  SA_CTL_Result_t SA_CTL_RequestWriteProperty_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_int64 value, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
        # self.SA_CTL_RequestWriteProperty_i64=wrapper(lib.SA_CTL_RequestWriteProperty_i64)
        # #  SA_CTL_Result_t SA_CTL_RequestWriteProperty_s(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_char_p value, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
        # self.SA_CTL_RequestWriteProperty_s=wrapper(lib.SA_CTL_RequestWriteProperty_s)
        # #  SA_CTL_Result_t SA_CTL_RequestWritePropertyArray_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int32) values, ctypes.c_size_t arraySize, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
        # self.SA_CTL_RequestWritePropertyArray_i32=wrapper(lib.SA_CTL_RequestWritePropertyArray_i32)
        # #  SA_CTL_Result_t SA_CTL_RequestWritePropertyArray_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int64) values, ctypes.c_size_t arraySize, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
        # self.SA_CTL_RequestWritePropertyArray_i64=wrapper(lib.SA_CTL_RequestWritePropertyArray_i64)
        # #  SA_CTL_Result_t SA_CTL_WaitForWrite(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID)
        # self.SA_CTL_WaitForWrite=wrapper(lib.SA_CTL_WaitForWrite)
        # #  SA_CTL_Result_t SA_CTL_CancelRequest(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID)
        # self.SA_CTL_CancelRequest=wrapper(lib.SA_CTL_CancelRequest)

    def SA_CTL_GetPropertyArray_i32(self, dHandle, idx, pkey, ioArraySize):
        v=(ctypes.c_int32*ioArraySize)()
        res=self.SA_CTL_GetProperty_i32_lib(dHandle,idx,pkey,v,ioArraySize)
        return list(v),res
    def SA_CTL_GetPropertyArray_i64(self, dHandle, idx, pkey, ioArraySize):
        v=(ctypes.c_int64*ioArraySize)()
        res=self.SA_CTL_GetProperty_i64_lib(dHandle,idx,pkey,v,ioArraySize)
        return list(v),res


wlib=SmarActControlLib()