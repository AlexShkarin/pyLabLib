##########   This file is generated automatically based on SmarActControl.h, SmarActControlConstants.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class SA_CTL(enum.IntEnum):
    SA_CTL_INFINITE                 = _int32(0xffffffff)
    SA_CTL_DISABLED                 = _int32(0x00)
    SA_CTL_ENABLED                  = _int32(0x01)
    SA_CTL_NON_INVERTED             = _int32(0x00)
    SA_CTL_INVERTED                 = _int32(0x01)
    SA_CTL_FORWARD_DIRECTION        = _int32(0x00)
    SA_CTL_BACKWARD_DIRECTION       = _int32(0x01)
    SA_CTL_EITHER_DIRECTION         = _int32(0x02)
    SA_CTL_STRING_MAX_LENGTH        = _int32(63)
    SA_CTL_REQUEST_ID_MAX_COUNT     = _int32(240)
    SA_CTL_POS_WRITE_PROTECTION_KEY = _int32(0x534D4152)
dSA_CTL={a.name:a.value for a in SA_CTL}
drSA_CTL={a.value:a.name for a in SA_CTL}


class SA_CTL_EVENT(enum.IntEnum):
    SA_CTL_EVENT_NONE                     = _int32(0x0000)
    SA_CTL_EVENT_MOVEMENT_FINISHED        = _int32(0x0001)
    SA_CTL_EVENT_SENSOR_STATE_CHANGED     = _int32(0x0002)
    SA_CTL_EVENT_REFERENCE_FOUND          = _int32(0x0003)
    SA_CTL_EVENT_FOLLOWING_ERR_LIMIT      = _int32(0x0004)
    SA_CTL_EVENT_HOLDING_ABORTED          = _int32(0x0005)
    SA_CTL_EVENT_SM_STATE_CHANGED         = _int32(0x4000)
    SA_CTL_EVENT_OVER_TEMPERATURE         = _int32(0x4001)
    SA_CTL_EVENT_HIGH_VOLTAGE_OVERLOAD    = _int32(0x4002)
    SA_CTL_EVENT_ADJUSTMENT_FINISHED      = _int32(0x4010)
    SA_CTL_EVENT_ADJUSTMENT_STATE_CHANGED = _int32(0x4011)
    SA_CTL_EVENT_ADJUSTMENT_UPDATE        = _int32(0x4012)
    SA_CTL_EVENT_DIGITAL_INPUT_CHANGED    = _int32(0x4040)
    SA_CTL_EVENT_STREAM_FINISHED          = _int32(0x8000)
    SA_CTL_EVENT_STREAM_READY             = _int32(0x8001)
    SA_CTL_EVENT_STREAM_TRIGGERED         = _int32(0x8002)
    SA_CTL_EVENT_CMD_GROUP_TRIGGERED      = _int32(0x8010)
    SA_CTL_EVENT_HM_STATE_CHANGED         = _int32(0x8020)
    SA_CTL_EVENT_EMERGENCY_STOP_TRIGGERED = _int32(0x8030)
    SA_CTL_EVENT_EXT_INPUT_TRIGGERED      = _int32(0x8040)
    SA_CTL_EVENT_BUS_RESYNC_TRIGGERED     = _int32(0x8050)
    SA_CTL_EVENT_REQUEST_READY            = _int32(0xf000)
    SA_CTL_EVENT_CONNECTION_LOST          = _int32(0xf001)
dSA_CTL_EVENT={a.name:a.value for a in SA_CTL_EVENT}
drSA_CTL_EVENT={a.value:a.name for a in SA_CTL_EVENT}


class SA_CTL_EVENT_PARAM(enum.IntEnum):
    SA_CTL_EVENT_PARAM_DETACHED              = _int32(0x00000000)
    SA_CTL_EVENT_PARAM_ATTACHED              = _int32(0x00000001)
    SA_CTL_EVENT_REQ_READY_TYPE_READ         = _int32(0x00)
    SA_CTL_EVENT_REQ_READY_TYPE_WRITE        = _int32(0x01)
    SA_CTL_EVENT_PARAM_RESULT_MASK           = _int32(0x0000ffff)
    SA_CTL_EVENT_PARAM_INDEX_MASK            = _int32(0x00ff0000)
    SA_CTL_EVENT_PARAM_HANDLE_MASK           = _int32(0xff000000)
    SA_CTL_EVENT_REQ_READY_ID_MASK           = _int32(0x00000000000000ff)
    SA_CTL_EVENT_REQ_READY_TYPE_MASK         = _int32(0x000000000000ff00)
    SA_CTL_EVENT_REQ_READY_DATA_TYPE_MASK    = _int32(0x0000000000ff0000)
    SA_CTL_EVENT_REQ_READY_ARRAY_SIZE_MASK   = _int32(0x00000000ff000000)
    SA_CTL_EVENT_REQ_READY_PROPERTY_KEY_MASK = _int32(0xffffffff00000000)
dSA_CTL_EVENT_PARAM={a.name:a.value for a in SA_CTL_EVENT_PARAM}
drSA_CTL_EVENT_PARAM={a.value:a.name for a in SA_CTL_EVENT_PARAM}


class SA_CTL_ERROR(enum.IntEnum):
    SA_CTL_ERROR_NONE                         = _int32(0x0000)
    SA_CTL_ERROR_UNKNOWN_COMMAND              = _int32(0x0001)
    SA_CTL_ERROR_INVALID_PACKET_SIZE          = _int32(0x0002)
    SA_CTL_ERROR_TIMEOUT                      = _int32(0x0004)
    SA_CTL_ERROR_INVALID_PROTOCOL             = _int32(0x0005)
    SA_CTL_ERROR_BUFFER_UNDERFLOW             = _int32(0x000c)
    SA_CTL_ERROR_BUFFER_OVERFLOW              = _int32(0x000d)
    SA_CTL_ERROR_INVALID_FRAME_SIZE           = _int32(0x000e)
    SA_CTL_ERROR_INVALID_PACKET               = _int32(0x0010)
    SA_CTL_ERROR_INVALID_KEY                  = _int32(0x0012)
    SA_CTL_ERROR_INVALID_PARAMETER            = _int32(0x0013)
    SA_CTL_ERROR_INVALID_DATA_TYPE            = _int32(0x0016)
    SA_CTL_ERROR_INVALID_DATA                 = _int32(0x0017)
    SA_CTL_ERROR_HANDLE_LIMIT_REACHED         = _int32(0x0018)
    SA_CTL_ERROR_ABORTED                      = _int32(0x0019)
    SA_CTL_ERROR_INVALID_DEVICE_INDEX         = _int32(0x0020)
    SA_CTL_ERROR_INVALID_MODULE_INDEX         = _int32(0x0021)
    SA_CTL_ERROR_INVALID_CHANNEL_INDEX        = _int32(0x0022)
    SA_CTL_ERROR_PERMISSION_DENIED            = _int32(0x0023)
    SA_CTL_ERROR_COMMAND_NOT_GROUPABLE        = _int32(0x0024)
    SA_CTL_ERROR_MOVEMENT_LOCKED              = _int32(0x0025)
    SA_CTL_ERROR_SYNC_FAILED                  = _int32(0x0026)
    SA_CTL_ERROR_INVALID_ARRAY_SIZE           = _int32(0x0027)
    SA_CTL_ERROR_OVERRANGE                    = _int32(0x0028)
    SA_CTL_ERROR_INVALID_CONFIGURATION        = _int32(0x0029)
    SA_CTL_ERROR_NO_HM_PRESENT                = _int32(0x0100)
    SA_CTL_ERROR_NO_IOM_PRESENT               = _int32(0x0101)
    SA_CTL_ERROR_NO_SM_PRESENT                = _int32(0x0102)
    SA_CTL_ERROR_NO_SENSOR_PRESENT            = _int32(0x0103)
    SA_CTL_ERROR_SENSOR_DISABLED              = _int32(0x0104)
    SA_CTL_ERROR_POWER_SUPPLY_DISABLED        = _int32(0x0105)
    SA_CTL_ERROR_AMPLIFIER_DISABLED           = _int32(0x0106)
    SA_CTL_ERROR_INVALID_SENSOR_MODE          = _int32(0x0107)
    SA_CTL_ERROR_INVALID_ACTUATOR_MODE        = _int32(0x0108)
    SA_CTL_ERROR_INVALID_INPUT_TRIG_MODE      = _int32(0x0109)
    SA_CTL_ERROR_INVALID_CONTROL_OPTIONS      = _int32(0x010a)
    SA_CTL_ERROR_INVALID_REFERENCE_TYPE       = _int32(0x010b)
    SA_CTL_ERROR_INVALID_ADJUSTMENT_STATE     = _int32(0x010c)
    SA_CTL_ERROR_INVALID_INFO_TYPE            = _int32(0x010d)
    SA_CTL_ERROR_NO_FULL_ACCESS               = _int32(0x010e)
    SA_CTL_ERROR_ADJUSTMENT_FAILED            = _int32(0x010f)
    SA_CTL_ERROR_MOVEMENT_OVERRIDDEN          = _int32(0x0110)
    SA_CTL_ERROR_NOT_CALIBRATED               = _int32(0x0111)
    SA_CTL_ERROR_NOT_REFERENCED               = _int32(0x0112)
    SA_CTL_ERROR_NOT_ADJUSTED                 = _int32(0x0113)
    SA_CTL_ERROR_SENSOR_TYPE_NOT_SUPPORTED    = _int32(0x0114)
    SA_CTL_ERROR_CONTROL_LOOP_INPUT_DISABLED  = _int32(0x0115)
    SA_CTL_ERROR_INVALID_CONTROL_LOOP_INPUT   = _int32(0x0116)
    SA_CTL_ERROR_UNEXPECTED_SENSOR_DATA       = _int32(0x0117)
    SA_CTL_ERROR_BUSY_MOVING                  = _int32(0x0150)
    SA_CTL_ERROR_BUSY_CALIBRATING             = _int32(0x0151)
    SA_CTL_ERROR_BUSY_REFERENCING             = _int32(0x0152)
    SA_CTL_ERROR_BUSY_ADJUSTING               = _int32(0x0153)
    SA_CTL_ERROR_END_STOP_REACHED             = _int32(0x0200)
    SA_CTL_ERROR_FOLLOWING_ERR_LIMIT          = _int32(0x0201)
    SA_CTL_ERROR_RANGE_LIMIT_REACHED          = _int32(0x0202)
    SA_CTL_ERROR_INVALID_STREAM_HANDLE        = _int32(0x0300)
    SA_CTL_ERROR_INVALID_STREAM_CONFIGURATION = _int32(0x0301)
    SA_CTL_ERROR_INSUFFICIENT_FRAMES          = _int32(0x0302)
    SA_CTL_ERROR_BUSY_STREAMING               = _int32(0x0303)
    SA_CTL_ERROR_HM_INVALID_SLOT_INDEX        = _int32(0x0400)
    SA_CTL_ERROR_HM_INVALID_CHANNEL_INDEX     = _int32(0x0401)
    SA_CTL_ERROR_HM_INVALID_GROUP_INDEX       = _int32(0x0402)
    SA_CTL_ERROR_HM_INVALID_CH_GRP_INDEX      = _int32(0x0403)
    SA_CTL_ERROR_INTERNAL_COMMUNICATION       = _int32(0x0500)
    SA_CTL_ERROR_FEATURE_NOT_SUPPORTED        = _int32(0x7ffd)
    SA_CTL_ERROR_FEATURE_NOT_IMPLEMENTED      = _int32(0x7ffe)
    SA_CTL_ERROR_DEVICE_LIMIT_REACHED         = _int32(0xf000)
    SA_CTL_ERROR_INVALID_LOCATOR              = _int32(0xf001)
    SA_CTL_ERROR_INITIALIZATION_FAILED        = _int32(0xf002)
    SA_CTL_ERROR_NOT_INITIALIZED              = _int32(0xf003)
    SA_CTL_ERROR_COMMUNICATION_FAILED         = _int32(0xf004)
    SA_CTL_ERROR_INVALID_QUERYBUFFER_SIZE     = _int32(0xf006)
    SA_CTL_ERROR_INVALID_DEVICE_HANDLE        = _int32(0xf007)
    SA_CTL_ERROR_INVALID_TRANSMIT_HANDLE      = _int32(0xf008)
    SA_CTL_ERROR_UNEXPECTED_PACKET_RECEIVED   = _int32(0xf00f)
    SA_CTL_ERROR_CANCELED                     = _int32(0xf010)
    SA_CTL_ERROR_DRIVER_FAILED                = _int32(0xf013)
    SA_CTL_ERROR_BUFFER_LIMIT_REACHED         = _int32(0xf016)
    SA_CTL_ERROR_INVALID_PROTOCOL_VERSION     = _int32(0xf017)
    SA_CTL_ERROR_DEVICE_RESET_FAILED          = _int32(0xf018)
    SA_CTL_ERROR_BUFFER_EMPTY                 = _int32(0xf019)
    SA_CTL_ERROR_DEVICE_NOT_FOUND             = _int32(0xf01a)
    SA_CTL_ERROR_THREAD_LIMIT_REACHED         = _int32(0xf01b)
dSA_CTL_ERROR={a.name:a.value for a in SA_CTL_ERROR}
drSA_CTL_ERROR={a.value:a.name for a in SA_CTL_ERROR}


class SA_CTL_DTYPE(enum.IntEnum):
    SA_CTL_DTYPE_UINT16  = _int32(0x03)
    SA_CTL_DTYPE_INT32   = _int32(0x06)
    SA_CTL_DTYPE_INT64   = _int32(0x0e)
    SA_CTL_DTYPE_FLOAT32 = _int32(0x10)
    SA_CTL_DTYPE_FLOAT64 = _int32(0x11)
    SA_CTL_DTYPE_STRING  = _int32(0x12)
    SA_CTL_DTYPE_NONE    = _int32(0xff)
dSA_CTL_DTYPE={a.name:a.value for a in SA_CTL_DTYPE}
drSA_CTL_DTYPE={a.value:a.name for a in SA_CTL_DTYPE}


class SA_CTL_UNIT(enum.IntEnum):
    SA_CTL_UNIT_NONE    = _int32(0x00000000)
    SA_CTL_UNIT_PERCENT = _int32(0x00000001)
    SA_CTL_UNIT_METER   = _int32(0x00000002)
    SA_CTL_UNIT_DEGREE  = _int32(0x00000003)
    SA_CTL_UNIT_SECOND  = _int32(0x00000004)
    SA_CTL_UNIT_HERTZ   = _int32(0x00000005)
dSA_CTL_UNIT={a.name:a.value for a in SA_CTL_UNIT}
drSA_CTL_UNIT={a.value:a.name for a in SA_CTL_UNIT}


class SA_CTL_PKEY(enum.IntEnum):
    SA_CTL_PKEY_NUMBER_OF_CHANNELS             = _int32(0x020F0017)
    SA_CTL_PKEY_NUMBER_OF_BUS_MODULES          = _int32(0x020F0016)
    SA_CTL_PKEY_DEVICE_STATE                   = _int32(0x020F000F)
    SA_CTL_PKEY_DEVICE_SERIAL_NUMBER           = _int32(0x020F005E)
    SA_CTL_PKEY_DEVICE_NAME                    = _int32(0x020F003D)
    SA_CTL_PKEY_EMERGENCY_STOP_MODE            = _int32(0x020F0088)
    SA_CTL_PKEY_NETWORK_DISCOVER_MODE          = _int32(0x020F0159)
    SA_CTL_PKEY_POWER_SUPPLY_ENABLED           = _int32(0x02030010)
    SA_CTL_PKEY_MODULE_STATE                   = _int32(0x0203000F)
    SA_CTL_PKEY_NUMBER_OF_BUS_MODULE_CHANNELS  = _int32(0x02030017)
    SA_CTL_PKEY_AMPLIFIER_ENABLED              = _int32(0x0302000D)
    SA_CTL_PKEY_POSITIONER_CONTROL_OPTIONS     = _int32(0x0302005D)
    SA_CTL_PKEY_ACTUATOR_MODE                  = _int32(0x03020019)
    SA_CTL_PKEY_CONTROL_LOOP_INPUT             = _int32(0x03020018)
    SA_CTL_PKEY_SENSOR_INPUT_SELECT            = _int32(0x0302009D)
    SA_CTL_PKEY_POSITIONER_TYPE                = _int32(0x0302003C)
    SA_CTL_PKEY_POSITIONER_TYPE_NAME           = _int32(0x0302003D)
    SA_CTL_PKEY_MOVE_MODE                      = _int32(0x03050087)
    SA_CTL_PKEY_CHANNEL_STATE                  = _int32(0x0305000F)
    SA_CTL_PKEY_POSITION                       = _int32(0x0305001D)
    SA_CTL_PKEY_TARGET_POSITION                = _int32(0x0305001E)
    SA_CTL_PKEY_SCAN_POSITION                  = _int32(0x0305001F)
    SA_CTL_PKEY_SCAN_VELOCITY                  = _int32(0x0305002A)
    SA_CTL_PKEY_HOLD_TIME                      = _int32(0x03050028)
    SA_CTL_PKEY_MOVE_VELOCITY                  = _int32(0x03050029)
    SA_CTL_PKEY_MOVE_ACCELERATION              = _int32(0x0305002B)
    SA_CTL_PKEY_MAX_CL_FREQUENCY               = _int32(0x0305002F)
    SA_CTL_PKEY_DEFAULT_MAX_CL_FREQUENCY       = _int32(0x03050057)
    SA_CTL_PKEY_STEP_FREQUENCY                 = _int32(0x0305002E)
    SA_CTL_PKEY_STEP_AMPLITUDE                 = _int32(0x03050030)
    SA_CTL_PKEY_FOLLOWING_ERROR_LIMIT          = _int32(0x03050055)
    SA_CTL_PKEY_FOLLOWING_ERROR                = _int32(0x03020055)
    SA_CTL_PKEY_BROADCAST_STOP_OPTIONS         = _int32(0x0305005D)
    SA_CTL_PKEY_SENSOR_POWER_MODE              = _int32(0x03080019)
    SA_CTL_PKEY_SENSOR_POWER_SAVE_DELAY        = _int32(0x03080054)
    SA_CTL_PKEY_POSITION_MEAN_SHIFT            = _int32(0x03090022)
    SA_CTL_PKEY_SAFE_DIRECTION                 = _int32(0x03090027)
    SA_CTL_PKEY_CL_INPUT_SENSOR_VALUE          = _int32(0x0302001D)
    SA_CTL_PKEY_CL_INPUT_AUX_VALUE             = _int32(0x030200B2)
    SA_CTL_PKEY_LOGICAL_SCALE_OFFSET           = _int32(0x02040024)
    SA_CTL_PKEY_LOGICAL_SCALE_INVERSION        = _int32(0x02040025)
    SA_CTL_PKEY_RANGE_LIMIT_MIN                = _int32(0x02040020)
    SA_CTL_PKEY_RANGE_LIMIT_MAX                = _int32(0x02040021)
    SA_CTL_PKEY_CALIBRATION_OPTIONS            = _int32(0x0306005D)
    SA_CTL_PKEY_SIGNAL_CORRECTION_OPTIONS      = _int32(0x0306001C)
    SA_CTL_PKEY_REFERENCING_OPTIONS            = _int32(0x0307005D)
    SA_CTL_PKEY_DIST_CODE_INVERTED             = _int32(0x0307000E)
    SA_CTL_PKEY_DISTANCE_TO_REF_MARK           = _int32(0x030700A2)
    SA_CTL_PKEY_POS_MOVEMENT_TYPE              = _int32(0x0309003F)
    SA_CTL_PKEY_POS_IS_CUSTOM_TYPE             = _int32(0x03090041)
    SA_CTL_PKEY_POS_BASE_UNIT                  = _int32(0x03090042)
    SA_CTL_PKEY_POS_BASE_RESOLUTION            = _int32(0x03090043)
    SA_CTL_PKEY_POS_P_GAIN                     = _int32(0x0309004B)
    SA_CTL_PKEY_POS_I_GAIN                     = _int32(0x0309004C)
    SA_CTL_PKEY_POS_D_GAIN                     = _int32(0x0309004D)
    SA_CTL_PKEY_POS_PID_SHIFT                  = _int32(0x0309004E)
    SA_CTL_PKEY_POS_ANTI_WINDUP                = _int32(0x0309004F)
    SA_CTL_PKEY_POS_ESD_DIST_TH                = _int32(0x03090050)
    SA_CTL_PKEY_POS_ESD_COUNTER_TH             = _int32(0x03090051)
    SA_CTL_PKEY_POS_TARGET_REACHED_TH          = _int32(0x03090052)
    SA_CTL_PKEY_POS_SAVE                       = _int32(0x0309000A)
    SA_CTL_PKEY_POS_WRITE_PROTECTION           = _int32(0x0309000D)
    SA_CTL_PKEY_STREAM_BASE_RATE               = _int32(0x040F002C)
    SA_CTL_PKEY_STREAM_EXT_SYNC_RATE           = _int32(0x040F002D)
    SA_CTL_PKEY_STREAM_OPTIONS                 = _int32(0x040F005D)
    SA_CTL_PKEY_CHANNEL_ERROR                  = _int32(0x0502007A)
    SA_CTL_PKEY_CHANNEL_TEMPERATURE            = _int32(0x05020034)
    SA_CTL_PKEY_BUS_MODULE_TEMPERATURE         = _int32(0x05030034)
    SA_CTL_PKEY_IO_MODULE_OPTIONS              = _int32(0x0603005D)
    SA_CTL_PKEY_IO_MODULE_VOLTAGE              = _int32(0x06030031)
    SA_CTL_PKEY_IO_MODULE_ANALOG_INPUT_RANGE   = _int32(0x060300A0)
    SA_CTL_PKEY_AUX_POSITIONER_TYPE            = _int32(0x0802003C)
    SA_CTL_PKEY_AUX_POSITIONER_TYPE_NAME       = _int32(0x0802003D)
    SA_CTL_PKEY_AUX_INPUT_SELECT               = _int32(0x08020018)
    SA_CTL_PKEY_AUX_IO_MODULE_INPUT_INDEX      = _int32(0x081100AA)
    SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT_INDEX  = _int32(0x080B00AA)
    SA_CTL_PKEY_AUX_IO_MODULE_INPUT0_VALUE     = _int32(0x08110000)
    SA_CTL_PKEY_AUX_IO_MODULE_INPUT1_VALUE     = _int32(0x08110001)
    SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT0_VALUE = _int32(0x080B0000)
    SA_CTL_PKEY_AUX_SENSOR_MODULE_INPUT1_VALUE = _int32(0x080B0001)
    SA_CTL_PKEY_AUX_DIRECTION_INVERSION        = _int32(0x0809000E)
    SA_CTL_PKEY_AUX_DIGITAL_INPUT_VALUE        = _int32(0x080300AD)
    SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_VALUE       = _int32(0x080300AE)
    SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_SET         = _int32(0x080300B0)
    SA_CTL_PKEY_AUX_DIGITAL_OUTPUT_CLEAR       = _int32(0x080300B1)
    SA_CTL_PKEY_AUX_ANALOG_OUTPUT_VALUE0       = _int32(0x08030000)
    SA_CTL_PKEY_AUX_ANALOG_OUTPUT_VALUE1       = _int32(0x08030001)
    SA_CTL_PKEY_THD_INPUT_SELECT               = _int32(0x09020018)
    SA_CTL_PKEY_THD_IO_MODULE_INPUT_INDEX      = _int32(0x091100AA)
    SA_CTL_PKEY_THD_SENSOR_MODULE_INPUT_INDEX  = _int32(0x090B00AA)
    SA_CTL_PKEY_THD_THRESHOLD_HIGH             = _int32(0x090200B4)
    SA_CTL_PKEY_THD_THRESHOLD_LOW              = _int32(0x090200B5)
    SA_CTL_PKEY_THD_INVERSION                  = _int32(0x0902000E)
    SA_CTL_PKEY_DEV_INPUT_TRIG_MODE            = _int32(0x060D0087)
    SA_CTL_PKEY_DEV_INPUT_TRIG_CONDITION       = _int32(0x060D005A)
    SA_CTL_PKEY_CH_OUTPUT_TRIG_MODE            = _int32(0x060E0087)
    SA_CTL_PKEY_CH_OUTPUT_TRIG_POLARITY        = _int32(0x060E005B)
    SA_CTL_PKEY_CH_OUTPUT_TRIG_PULSE_WIDTH     = _int32(0x060E005C)
    SA_CTL_PKEY_CH_POS_COMP_START_THRESHOLD    = _int32(0x060E0058)
    SA_CTL_PKEY_CH_POS_COMP_INCREMENT          = _int32(0x060E0059)
    SA_CTL_PKEY_CH_POS_COMP_DIRECTION          = _int32(0x060E0026)
    SA_CTL_PKEY_CH_POS_COMP_LIMIT_MIN          = _int32(0x060E0020)
    SA_CTL_PKEY_CH_POS_COMP_LIMIT_MAX          = _int32(0x060E0021)
    SA_CTL_PKEY_HM_STATE                       = _int32(0x020C000F)
    SA_CTL_PKEY_HM_LOCK_OPTIONS                = _int32(0x020C0083)
    SA_CTL_PKEY_HM_DEFAULT_LOCK_OPTIONS        = _int32(0x020C0084)
    SA_CTL_PKEY_EVENT_NOTIFICATION_OPTIONS     = _int32(0xF010005D)
    SA_CTL_PKEY_AUTO_RECONNECT                 = _int32(0xF01000A1)
dSA_CTL_PKEY={a.name:a.value for a in SA_CTL_PKEY}
drSA_CTL_PKEY={a.value:a.name for a in SA_CTL_PKEY}


class SA_CTL_DEV_STATE(enum.IntEnum):
    SA_CTL_DEV_STATE_BIT_HM_PRESENT            = _int32(0x0001)
    SA_CTL_DEV_STATE_BIT_MOVEMENT_LOCKED       = _int32(0x0002)
    SA_CTL_DEV_STATE_BIT_INTERNAL_COMM_FAILURE = _int32(0x0100)
    SA_CTL_DEV_STATE_BIT_IS_STREAMING          = _int32(0x1000)
dSA_CTL_DEV_STATE={a.name:a.value for a in SA_CTL_DEV_STATE}
drSA_CTL_DEV_STATE={a.value:a.name for a in SA_CTL_DEV_STATE}


class SA_CTL_MOD_STATE(enum.IntEnum):
    SA_CTL_MOD_STATE_BIT_SM_PRESENT            = _int32(0x0001)
    SA_CTL_MOD_STATE_BIT_BOOSTER_PRESENT       = _int32(0x0002)
    SA_CTL_MOD_STATE_BIT_ADJUSTMENT_ACTIVE     = _int32(0x0004)
    SA_CTL_MOD_STATE_BIT_IOM_PRESENT           = _int32(0x0008)
    SA_CTL_MOD_STATE_BIT_INTERNAL_COMM_FAILURE = _int32(0x0100)
    SA_CTL_MOD_STATE_BIT_HIGH_VOLTAGE_FAILURE  = _int32(0x1000)
    SA_CTL_MOD_STATE_BIT_HIGH_VOLTAGE_OVERLOAD = _int32(0x2000)
    SA_CTL_MOD_STATE_BIT_OVER_TEMPERATURE      = _int32(0x4000)
dSA_CTL_MOD_STATE={a.name:a.value for a in SA_CTL_MOD_STATE}
drSA_CTL_MOD_STATE={a.value:a.name for a in SA_CTL_MOD_STATE}


class SA_CTL_CH_STATE(enum.IntEnum):
    SA_CTL_CH_STATE_BIT_ACTIVELY_MOVING         = _int32(0x0001)
    SA_CTL_CH_STATE_BIT_CLOSED_LOOP_ACTIVE      = _int32(0x0002)
    SA_CTL_CH_STATE_BIT_CALIBRATING             = _int32(0x0004)
    SA_CTL_CH_STATE_BIT_REFERENCING             = _int32(0x0008)
    SA_CTL_CH_STATE_BIT_MOVE_DELAYED            = _int32(0x0010)
    SA_CTL_CH_STATE_BIT_SENSOR_PRESENT          = _int32(0x0020)
    SA_CTL_CH_STATE_BIT_IS_CALIBRATED           = _int32(0x0040)
    SA_CTL_CH_STATE_BIT_IS_REFERENCED           = _int32(0x0080)
    SA_CTL_CH_STATE_BIT_END_STOP_REACHED        = _int32(0x0100)
    SA_CTL_CH_STATE_BIT_RANGE_LIMIT_REACHED     = _int32(0x0200)
    SA_CTL_CH_STATE_BIT_FOLLOWING_LIMIT_REACHED = _int32(0x0400)
    SA_CTL_CH_STATE_BIT_MOVEMENT_FAILED         = _int32(0x0800)
    SA_CTL_CH_STATE_BIT_IS_STREAMING            = _int32(0x1000)
    SA_CTL_CH_STATE_BIT_OVER_TEMPERATURE        = _int32(0x4000)
    SA_CTL_CH_STATE_BIT_REFERENCE_MARK          = _int32(0x8000)
dSA_CTL_CH_STATE={a.name:a.value for a in SA_CTL_CH_STATE}
drSA_CTL_CH_STATE={a.value:a.name for a in SA_CTL_CH_STATE}


class SA_CTL_HM_STATE(enum.IntEnum):
    SA_CTL_HM_STATE_BIT_INTERNAL_COMM_FAILURE = _int32(0x0100)
    SA_CTL_HM_STATE_BIT_IS_INTERNAL           = _int32(0x0200)
dSA_CTL_HM_STATE={a.name:a.value for a in SA_CTL_HM_STATE}
drSA_CTL_HM_STATE={a.value:a.name for a in SA_CTL_HM_STATE}


class SA_CTL_MOVE_MODE(enum.IntEnum):
    SA_CTL_MOVE_MODE_CL_ABSOLUTE   = _int32(0)
    SA_CTL_MOVE_MODE_CL_RELATIVE   = _int32(1)
    SA_CTL_MOVE_MODE_SCAN_ABSOLUTE = _int32(2)
    SA_CTL_MOVE_MODE_SCAN_RELATIVE = _int32(3)
    SA_CTL_MOVE_MODE_STEP          = _int32(4)
dSA_CTL_MOVE_MODE={a.name:a.value for a in SA_CTL_MOVE_MODE}
drSA_CTL_MOVE_MODE={a.value:a.name for a in SA_CTL_MOVE_MODE}


class SA_CTL_ACTUATOR_MODE(enum.IntEnum):
    SA_CTL_ACTUATOR_MODE_NORMAL        = _int32(0)
    SA_CTL_ACTUATOR_MODE_QUIET         = _int32(1)
    SA_CTL_ACTUATOR_MODE_LOW_VIBRATION = _int32(2)
dSA_CTL_ACTUATOR_MODE={a.name:a.value for a in SA_CTL_ACTUATOR_MODE}
drSA_CTL_ACTUATOR_MODE={a.value:a.name for a in SA_CTL_ACTUATOR_MODE}


class SA_CTL_CONTROL_LOOP(enum.IntEnum):
    SA_CTL_CONTROL_LOOP_INPUT_DISABLED = _int32(0)
    SA_CTL_CONTROL_LOOP_INPUT_SENSOR   = _int32(1)
    SA_CTL_CONTROL_LOOP_INPUT_POSITION = _int32(1)
    SA_CTL_CONTROL_LOOP_INPUT_AUX_IN   = _int32(2)
dSA_CTL_CONTROL_LOOP={a.name:a.value for a in SA_CTL_CONTROL_LOOP}
drSA_CTL_CONTROL_LOOP={a.value:a.name for a in SA_CTL_CONTROL_LOOP}


class SA_CTL_SENSOR_INPUT(enum.IntEnum):
    SA_CTL_SENSOR_INPUT_SELECT_POSITION = _int32(0)
    SA_CTL_SENSOR_INPUT_SELECT_CALC_SYS = _int32(1)
dSA_CTL_SENSOR_INPUT={a.name:a.value for a in SA_CTL_SENSOR_INPUT}
drSA_CTL_SENSOR_INPUT={a.value:a.name for a in SA_CTL_SENSOR_INPUT}


class SA_CTL_AUX_INPUT_SELECT(enum.IntEnum):
    SA_CTL_AUX_INPUT_SELECT_IO_MODULE     = _int32(0)
    SA_CTL_AUX_INPUT_SELECT_SENSOR_MODULE = _int32(1)
dSA_CTL_AUX_INPUT_SELECT={a.name:a.value for a in SA_CTL_AUX_INPUT_SELECT}
drSA_CTL_AUX_INPUT_SELECT={a.value:a.name for a in SA_CTL_AUX_INPUT_SELECT}


class SA_CTL_THD_INPUT_SELECT(enum.IntEnum):
    SA_CTL_THD_INPUT_SELECT_IO_MODULE     = _int32(0)
    SA_CTL_THD_INPUT_SELECT_SENSOR_MODULE = _int32(1)
dSA_CTL_THD_INPUT_SELECT={a.name:a.value for a in SA_CTL_THD_INPUT_SELECT}
drSA_CTL_THD_INPUT_SELECT={a.value:a.name for a in SA_CTL_THD_INPUT_SELECT}


class SA_CTL_EMERGENCY_STOP(enum.IntEnum):
    SA_CTL_EMERGENCY_STOP_MODE_NORMAL       = _int32(0)
    SA_CTL_EMERGENCY_STOP_MODE_RESTRICTED   = _int32(1)
    SA_CTL_EMERGENCY_STOP_MODE_AUTO_RELEASE = _int32(2)
dSA_CTL_EMERGENCY_STOP={a.name:a.value for a in SA_CTL_EMERGENCY_STOP}
drSA_CTL_EMERGENCY_STOP={a.value:a.name for a in SA_CTL_EMERGENCY_STOP}


class SA_CTL_CMD_GROUP_TRIGGER_MODE(enum.IntEnum):
    SA_CTL_CMD_GROUP_TRIGGER_MODE_DIRECT   = _int32(0)
    SA_CTL_CMD_GROUP_TRIGGER_MODE_EXTERNAL = _int32(1)
dSA_CTL_CMD_GROUP_TRIGGER_MODE={a.name:a.value for a in SA_CTL_CMD_GROUP_TRIGGER_MODE}
drSA_CTL_CMD_GROUP_TRIGGER_MODE={a.value:a.name for a in SA_CTL_CMD_GROUP_TRIGGER_MODE}


class SA_CTL_STREAM_TRIGGER_MODE(enum.IntEnum):
    SA_CTL_STREAM_TRIGGER_MODE_DIRECT        = _int32(0)
    SA_CTL_STREAM_TRIGGER_MODE_EXTERNAL_ONCE = _int32(1)
    SA_CTL_STREAM_TRIGGER_MODE_EXTERNAL_SYNC = _int32(2)
dSA_CTL_STREAM_TRIGGER_MODE={a.name:a.value for a in SA_CTL_STREAM_TRIGGER_MODE}
drSA_CTL_STREAM_TRIGGER_MODE={a.value:a.name for a in SA_CTL_STREAM_TRIGGER_MODE}


class SA_CTL_STREAM_OPT_BIT(enum.IntEnum):
    SA_CTL_STREAM_OPT_BIT_INTERPOLATION_DIS = _int32(0x00000001)
dSA_CTL_STREAM_OPT_BIT={a.name:a.value for a in SA_CTL_STREAM_OPT_BIT}
drSA_CTL_STREAM_OPT_BIT={a.value:a.name for a in SA_CTL_STREAM_OPT_BIT}


class SA_CTL_POS_CTRL_OPT_BIT(enum.IntEnum):
    SA_CTL_POS_CTRL_OPT_BIT_ACC_REL_POS_DIS       = _int32(0x00000001)
    SA_CTL_POS_CTRL_OPT_BIT_NO_SLIP               = _int32(0x00000002)
    SA_CTL_POS_CTRL_OPT_BIT_NO_SLIP_WHILE_HOLDING = _int32(0x00000004)
    SA_CTL_POS_CTRL_OPT_BIT_FORCED_SLIP_DIS       = _int32(0x00000008)
    SA_CTL_POS_CTRL_OPT_BIT_STOP_ON_FOLLOWING_ERR = _int32(0x00000010)
dSA_CTL_POS_CTRL_OPT_BIT={a.name:a.value for a in SA_CTL_POS_CTRL_OPT_BIT}
drSA_CTL_POS_CTRL_OPT_BIT={a.value:a.name for a in SA_CTL_POS_CTRL_OPT_BIT}


class SA_CTL_CALIB_OPT_BIT(enum.IntEnum):
    SA_CTL_CALIB_OPT_BIT_DIRECTION            = _int32(0x00000001)
    SA_CTL_CALIB_OPT_BIT_DIST_CODE_INV_DETECT = _int32(0x00000002)
    SA_CTL_CALIB_OPT_BIT_ASC_CALIBRATION      = _int32(0x00000004)
    SA_CTL_CALIB_OPT_BIT_REF_MARK_TEST        = _int32(0x00000008)
    SA_CTL_CALIB_OPT_BIT_LIMITED_TRAVEL_RANGE = _int32(0x00000100)
dSA_CTL_CALIB_OPT_BIT={a.name:a.value for a in SA_CTL_CALIB_OPT_BIT}
drSA_CTL_CALIB_OPT_BIT={a.value:a.name for a in SA_CTL_CALIB_OPT_BIT}


class SA_CTL_REF_OPT_BIT(enum.IntEnum):
    SA_CTL_REF_OPT_BIT_START_DIR             = _int32(0x00000001)
    SA_CTL_REF_OPT_BIT_REVERSE_DIR           = _int32(0x00000002)
    SA_CTL_REF_OPT_BIT_AUTO_ZERO             = _int32(0x00000004)
    SA_CTL_REF_OPT_BIT_ABORT_ON_ENDSTOP      = _int32(0x00000008)
    SA_CTL_REF_OPT_BIT_CONTINUE_ON_REF_FOUND = _int32(0x00000010)
    SA_CTL_REF_OPT_BIT_STOP_ON_REF_FOUND     = _int32(0x00000020)
dSA_CTL_REF_OPT_BIT={a.name:a.value for a in SA_CTL_REF_OPT_BIT}
drSA_CTL_REF_OPT_BIT={a.value:a.name for a in SA_CTL_REF_OPT_BIT}


class SA_CTL_SENSOR_MODE(enum.IntEnum):
    SA_CTL_SENSOR_MODE_DISABLED   = _int32(0)
    SA_CTL_SENSOR_MODE_ENABLED    = _int32(1)
    SA_CTL_SENSOR_MODE_POWER_SAVE = _int32(2)
dSA_CTL_SENSOR_MODE={a.name:a.value for a in SA_CTL_SENSOR_MODE}
drSA_CTL_SENSOR_MODE={a.value:a.name for a in SA_CTL_SENSOR_MODE}


class SA_CTL_STOP_OPT_BIT(enum.IntEnum):
    SA_CTL_STOP_OPT_BIT_END_STOP_REACHED        = _int32(0x00000001)
    SA_CTL_STOP_OPT_BIT_RANGE_LIMIT_REACHED     = _int32(0x00000002)
    SA_CTL_STOP_OPT_BIT_FOLLOWING_LIMIT_REACHED = _int32(0x00000004)
dSA_CTL_STOP_OPT_BIT={a.name:a.value for a in SA_CTL_STOP_OPT_BIT}
drSA_CTL_STOP_OPT_BIT={a.value:a.name for a in SA_CTL_STOP_OPT_BIT}


class SA_CTL_DEV_INPUT_TRIG_MODE(enum.IntEnum):
    SA_CTL_DEV_INPUT_TRIG_MODE_DISABLED       = _int32(0)
    SA_CTL_DEV_INPUT_TRIG_MODE_EMERGENCY_STOP = _int32(1)
    SA_CTL_DEV_INPUT_TRIG_MODE_STREAM         = _int32(2)
    SA_CTL_DEV_INPUT_TRIG_MODE_CMD_GROUP      = _int32(3)
    SA_CTL_DEV_INPUT_TRIG_MODE_EVENT          = _int32(4)
dSA_CTL_DEV_INPUT_TRIG_MODE={a.name:a.value for a in SA_CTL_DEV_INPUT_TRIG_MODE}
drSA_CTL_DEV_INPUT_TRIG_MODE={a.value:a.name for a in SA_CTL_DEV_INPUT_TRIG_MODE}


class SA_CTL_CH_OUTPUT_TRIG_MODE(enum.IntEnum):
    SA_CTL_CH_OUTPUT_TRIG_MODE_CONSTANT         = _int32(0)
    SA_CTL_CH_OUTPUT_TRIG_MODE_POSITION_COMPARE = _int32(1)
    SA_CTL_CH_OUTPUT_TRIG_MODE_TARGET_REACHED   = _int32(2)
    SA_CTL_CH_OUTPUT_TRIG_MODE_ACTIVELY_MOVING  = _int32(3)
dSA_CTL_CH_OUTPUT_TRIG_MODE={a.name:a.value for a in SA_CTL_CH_OUTPUT_TRIG_MODE}
drSA_CTL_CH_OUTPUT_TRIG_MODE={a.value:a.name for a in SA_CTL_CH_OUTPUT_TRIG_MODE}


class SA_CTL_TRIGGER_CONDITION(enum.IntEnum):
    SA_CTL_TRIGGER_CONDITION_RISING  = _int32(0)
    SA_CTL_TRIGGER_CONDITION_FALLING = _int32(1)
    SA_CTL_TRIGGER_CONDITION_EITHER  = _int32(2)
dSA_CTL_TRIGGER_CONDITION={a.name:a.value for a in SA_CTL_TRIGGER_CONDITION}
drSA_CTL_TRIGGER_CONDITION={a.value:a.name for a in SA_CTL_TRIGGER_CONDITION}


class SA_CTL_TRIGGER_POLARITY(enum.IntEnum):
    SA_CTL_TRIGGER_POLARITY_ACTIVE_LOW  = _int32(0)
    SA_CTL_TRIGGER_POLARITY_ACTIVE_HIGH = _int32(1)
dSA_CTL_TRIGGER_POLARITY={a.name:a.value for a in SA_CTL_TRIGGER_POLARITY}
drSA_CTL_TRIGGER_POLARITY={a.value:a.name for a in SA_CTL_TRIGGER_POLARITY}


class SA_CTL_HM1_LOCK_OPT_BIT(enum.IntEnum):
    SA_CTL_HM1_LOCK_OPT_BIT_GLOBAL               = _int32(0x00000001)
    SA_CTL_HM1_LOCK_OPT_BIT_CONTROL              = _int32(0x00000002)
    SA_CTL_HM1_LOCK_OPT_BIT_CHANNEL_MENU         = _int32(0x00000010)
    SA_CTL_HM1_LOCK_OPT_BIT_GROUP_MENU           = _int32(0x00000020)
    SA_CTL_HM1_LOCK_OPT_BIT_SETTINGS_MENU        = _int32(0x00000040)
    SA_CTL_HM1_LOCK_OPT_BIT_LOAD_CFG_MENU        = _int32(0x00000080)
    SA_CTL_HM1_LOCK_OPT_BIT_SAVE_CFG_MENU        = _int32(0x00000100)
    SA_CTL_HM1_LOCK_OPT_BIT_CTRL_MODE_PARAM_MENU = _int32(0x00000200)
    SA_CTL_HM1_LOCK_OPT_BIT_CHANNEL_NAME         = _int32(0x00001000)
    SA_CTL_HM1_LOCK_OPT_BIT_POS_TYPE             = _int32(0x00002000)
    SA_CTL_HM1_LOCK_OPT_BIT_SAFE_DIR             = _int32(0x00004000)
    SA_CTL_HM1_LOCK_OPT_BIT_CALIBRATE            = _int32(0x00008000)
    SA_CTL_HM1_LOCK_OPT_BIT_REFERENCE            = _int32(0x00010000)
    SA_CTL_HM1_LOCK_OPT_BIT_SET_POSITION         = _int32(0x00020000)
    SA_CTL_HM1_LOCK_OPT_BIT_MAX_CLF              = _int32(0x00040000)
    SA_CTL_HM1_LOCK_OPT_BIT_POWER_MODE           = _int32(0x00080000)
    SA_CTL_HM1_LOCK_OPT_BIT_ACTUATOR_MODE        = _int32(0x00100000)
    SA_CTL_HM1_LOCK_OPT_BIT_RANGE_LIMIT          = _int32(0x00200000)
    SA_CTL_HM1_LOCK_OPT_BIT_CONTROL_LOOP_INPUT   = _int32(0x00400000)
dSA_CTL_HM1_LOCK_OPT_BIT={a.name:a.value for a in SA_CTL_HM1_LOCK_OPT_BIT}
drSA_CTL_HM1_LOCK_OPT_BIT={a.value:a.name for a in SA_CTL_HM1_LOCK_OPT_BIT}


class SA_CTL_EVT_OPT_BIT(enum.IntEnum):
    SA_CTL_EVT_OPT_BIT_REQUEST_READY_ENABLED = _int32(0x00000001)
dSA_CTL_EVT_OPT_BIT={a.name:a.value for a in SA_CTL_EVT_OPT_BIT}
drSA_CTL_EVT_OPT_BIT={a.value:a.name for a in SA_CTL_EVT_OPT_BIT}


class SA_CTL_POSITIONER_TYPE(enum.IntEnum):
    SA_CTL_POSITIONER_TYPE_CUSTOM0 = _int32(250)
    SA_CTL_POSITIONER_TYPE_CUSTOM1 = _int32(251)
    SA_CTL_POSITIONER_TYPE_CUSTOM2 = _int32(252)
    SA_CTL_POSITIONER_TYPE_CUSTOM3 = _int32(253)
dSA_CTL_POSITIONER_TYPE={a.name:a.value for a in SA_CTL_POSITIONER_TYPE}
drSA_CTL_POSITIONER_TYPE={a.value:a.name for a in SA_CTL_POSITIONER_TYPE}


class SA_CTL_POS_MOVEMENT_TYPE(enum.IntEnum):
    SA_CTL_POS_MOVEMENT_TYPE_LINEAR     = _int32(0)
    SA_CTL_POS_MOVEMENT_TYPE_ROTATORY   = _int32(1)
    SA_CTL_POS_MOVEMENT_TYPE_GONIOMETER = _int32(2)
    SA_CTL_POS_MOVEMENT_TYPE_TIP_TILT   = _int32(3)
    SA_CTL_POS_MOVEMENT_TYPE_IRIS       = _int32(4)
    SA_CTL_POS_MOVEMENT_TYPE_OSCILLATOR = _int32(5)
dSA_CTL_POS_MOVEMENT_TYPE={a.name:a.value for a in SA_CTL_POS_MOVEMENT_TYPE}
drSA_CTL_POS_MOVEMENT_TYPE={a.value:a.name for a in SA_CTL_POS_MOVEMENT_TYPE}


class SA_CTL_IO_MODULE_VOLTAGE(enum.IntEnum):
    SA_CTL_IO_MODULE_VOLTAGE_3V3 = _int32(0)
    SA_CTL_IO_MODULE_VOLTAGE_5V  = _int32(1)
dSA_CTL_IO_MODULE_VOLTAGE={a.name:a.value for a in SA_CTL_IO_MODULE_VOLTAGE}
drSA_CTL_IO_MODULE_VOLTAGE={a.value:a.name for a in SA_CTL_IO_MODULE_VOLTAGE}


class SA_CTL_IO_MODULE_OPT_BIT(enum.IntEnum):
    SA_CTL_IO_MODULE_OPT_BIT_ENABLED        = _int32(0x00000001)
    SA_CTL_IO_MODULE_OPT_BIT_EVENTS_ENABLED = _int32(0x00000002)
dSA_CTL_IO_MODULE_OPT_BIT={a.name:a.value for a in SA_CTL_IO_MODULE_OPT_BIT}
drSA_CTL_IO_MODULE_OPT_BIT={a.value:a.name for a in SA_CTL_IO_MODULE_OPT_BIT}


class SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE(enum.IntEnum):
    SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_BI_10V  = _int32(0)
    SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_BI_5V   = _int32(1)
    SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_BI_2_5V = _int32(2)
    SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_UNI_10V = _int32(3)
    SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE_UNI_5V  = _int32(4)
dSA_CTL_IO_MODULE_ANALOG_INPUT_RANGE={a.name:a.value for a in SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE}
drSA_CTL_IO_MODULE_ANALOG_INPUT_RANGE={a.value:a.name for a in SA_CTL_IO_MODULE_ANALOG_INPUT_RANGE}


class SA_CTL_SIGNAL_CORR_OPT_BIT(enum.IntEnum):
    SA_CTL_SIGNAL_CORR_OPT_BIT_DAC  = _int32(0x00000002)
    SA_CTL_SIGNAL_CORR_OPT_BIT_DPEC = _int32(0x00000008)
    SA_CTL_SIGNAL_CORR_OPT_BIT_ASC  = _int32(0x00000010)
dSA_CTL_SIGNAL_CORR_OPT_BIT={a.name:a.value for a in SA_CTL_SIGNAL_CORR_OPT_BIT}
drSA_CTL_SIGNAL_CORR_OPT_BIT={a.value:a.name for a in SA_CTL_SIGNAL_CORR_OPT_BIT}


class SA_CTL_NETWORK_DISCOVER_MODE(enum.IntEnum):
    SA_CTL_NETWORK_DISCOVER_MODE_DISABLED = _int32(0)
    SA_CTL_NETWORK_DISCOVER_MODE_PASSIVE  = _int32(1)
    SA_CTL_NETWORK_DISCOVER_MODE_ACTIVE   = _int32(2)
dSA_CTL_NETWORK_DISCOVER_MODE={a.name:a.value for a in SA_CTL_NETWORK_DISCOVER_MODE}
drSA_CTL_NETWORK_DISCOVER_MODE={a.value:a.name for a in SA_CTL_NETWORK_DISCOVER_MODE}





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
DWORD=ctypes.c_ulong
LPWORD=ctypes.POINTER(WORD)
LONG=ctypes.c_long
LONGLONG=ctypes.c_int64
LPLONG=ctypes.POINTER(ctypes.c_long)
HANDLE=ctypes.c_void_p
LPHANDLE=ctypes.POINTER(HANDLE)
PHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
class RECT(ctypes.Structure):
    _fields_=[  ("left",LONG),
                ("top",LONG),
                ("right",LONG),
                ("bottom",LONG) ]
PRECT=ctypes.POINTER(RECT)
class CRECT(ctypes_wrap.CStructWrapper):
    _struct=RECT


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_=[  ("biSize",DWORD),
                ("biWidth",LONG),
                ("biHeight",LONG),
                ("biPlanes",WORD),
                ("biBitCount",WORD),
                ("biCompression",DWORD),
                ("biSizeImage",DWORD),
                ("biXPelsPerMeter",LONG),
                ("biYPelsPerMeter",LONG),
                ("biClrUsed",DWORD),
                ("biClrImportant",DWORD) ]
PBITMAPINFOHEADER=ctypes.POINTER(BITMAPINFOHEADER)
class CBITMAPINFOHEADER(ctypes_wrap.CStructWrapper):
    _struct=BITMAPINFOHEADER


MirEGLNativeWindowType=ctypes.c_void_p
MirEGLNativeDisplayType=ctypes.c_void_p
SA_CTL_DeviceHandle_t=ctypes.c_uint32
SA_CTL_TransmitHandle_t=ctypes.c_uint32
SA_CTL_StreamHandle_t=ctypes.c_uint32
SA_CTL_RequestID_t=ctypes.c_uint8
SA_CTL_PropertyKey_t=ctypes.c_uint32
SA_CTL_Result_t=ctypes.c_uint32
class SA_CTL_Event_t(ctypes.Structure):
    _fields_=[  ("idx",ctypes.c_uint32),
                ("type",ctypes.c_uint32),
                ("value",ctypes.c_uint8*24) ]
PSA_CTL_Event_t=ctypes.POINTER(SA_CTL_Event_t)
class CSA_CTL_Event_t(ctypes_wrap.CStructWrapper):
    _struct=SA_CTL_Event_t





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
    #  ctypes.c_char_p SA_CTL_GetFullVersionString()
    addfunc(lib, "SA_CTL_GetFullVersionString", restype = ctypes.c_char_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_char_p SA_CTL_GetResultInfo(SA_CTL_Result_t result)
    addfunc(lib, "SA_CTL_GetResultInfo", restype = ctypes.c_char_p,
            argtypes = [SA_CTL_Result_t],
            argnames = ["result"] )
    #  ctypes.c_char_p SA_CTL_GetEventInfo(ctypes.POINTER(SA_CTL_Event_t) event)
    addfunc(lib, "SA_CTL_GetEventInfo", restype = ctypes.c_char_p,
            argtypes = [ctypes.POINTER(SA_CTL_Event_t)],
            argnames = ["event"] )
    #  SA_CTL_Result_t SA_CTL_Open(ctypes.POINTER(SA_CTL_DeviceHandle_t) dHandle, ctypes.c_char_p locator, ctypes.c_char_p config)
    addfunc(lib, "SA_CTL_Open", restype = SA_CTL_Result_t,
            argtypes = [ctypes.POINTER(SA_CTL_DeviceHandle_t), ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["dHandle", "locator", "config"] )
    #  SA_CTL_Result_t SA_CTL_Close(SA_CTL_DeviceHandle_t dHandle)
    addfunc(lib, "SA_CTL_Close", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t],
            argnames = ["dHandle"] )
    #  SA_CTL_Result_t SA_CTL_Cancel(SA_CTL_DeviceHandle_t dHandle)
    addfunc(lib, "SA_CTL_Cancel", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t],
            argnames = ["dHandle"] )
    #  SA_CTL_Result_t SA_CTL_FindDevices(ctypes.c_char_p options, ctypes.c_char_p deviceList, ctypes.POINTER(ctypes.c_size_t) deviceListLen)
    addfunc(lib, "SA_CTL_FindDevices", restype = SA_CTL_Result_t,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["options", "deviceList", "deviceListLen"] )
    #  SA_CTL_Result_t SA_CTL_GetProperty_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int32) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
    addfunc(lib, "SA_CTL_GetProperty_i32", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["dHandle", "idx", "pkey", "value", "ioArraySize"] )
    #  SA_CTL_Result_t SA_CTL_SetProperty_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_int32 value)
    addfunc(lib, "SA_CTL_SetProperty_i32", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.c_int32],
            argnames = ["dHandle", "idx", "pkey", "value"] )
    #  SA_CTL_Result_t SA_CTL_SetPropertyArray_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int32) values, ctypes.c_size_t arraySize)
    addfunc(lib, "SA_CTL_SetPropertyArray_i32", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t],
            argnames = ["dHandle", "idx", "pkey", "values", "arraySize"] )
    #  SA_CTL_Result_t SA_CTL_GetProperty_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int64) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
    addfunc(lib, "SA_CTL_GetProperty_i64", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["dHandle", "idx", "pkey", "value", "ioArraySize"] )
    #  SA_CTL_Result_t SA_CTL_SetProperty_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_int64 value)
    addfunc(lib, "SA_CTL_SetProperty_i64", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.c_int64],
            argnames = ["dHandle", "idx", "pkey", "value"] )
    #  SA_CTL_Result_t SA_CTL_SetPropertyArray_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int64) values, ctypes.c_size_t arraySize)
    addfunc(lib, "SA_CTL_SetPropertyArray_i64", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t],
            argnames = ["dHandle", "idx", "pkey", "values", "arraySize"] )
    #  SA_CTL_Result_t SA_CTL_GetProperty_s(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_char_p value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
    addfunc(lib, "SA_CTL_GetProperty_s", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["dHandle", "idx", "pkey", "value", "ioArraySize"] )
    #  SA_CTL_Result_t SA_CTL_SetProperty_s(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_char_p value)
    addfunc(lib, "SA_CTL_SetProperty_s", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.c_char_p],
            argnames = ["dHandle", "idx", "pkey", "value"] )
    #  SA_CTL_Result_t SA_CTL_RequestReadProperty(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_RequestReadProperty", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.POINTER(SA_CTL_RequestID_t), SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "pkey", "rID", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_ReadProperty_i32(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID, ctypes.POINTER(ctypes.c_int32) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
    addfunc(lib, "SA_CTL_ReadProperty_i32", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_RequestID_t, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["dHandle", "rID", "value", "ioArraySize"] )
    #  SA_CTL_Result_t SA_CTL_ReadProperty_i64(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID, ctypes.POINTER(ctypes.c_int64) value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
    addfunc(lib, "SA_CTL_ReadProperty_i64", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_RequestID_t, ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["dHandle", "rID", "value", "ioArraySize"] )
    #  SA_CTL_Result_t SA_CTL_ReadProperty_s(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID, ctypes.c_char_p value, ctypes.POINTER(ctypes.c_size_t) ioArraySize)
    addfunc(lib, "SA_CTL_ReadProperty_s", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_RequestID_t, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["dHandle", "rID", "value", "ioArraySize"] )
    #  SA_CTL_Result_t SA_CTL_RequestWriteProperty_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_int32 value, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_RequestWriteProperty_i32", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.c_int32, ctypes.POINTER(SA_CTL_RequestID_t), SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "pkey", "value", "rID", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_RequestWriteProperty_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_int64 value, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_RequestWriteProperty_i64", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.c_int64, ctypes.POINTER(SA_CTL_RequestID_t), SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "pkey", "value", "rID", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_RequestWriteProperty_s(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.c_char_p value, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_RequestWriteProperty_s", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.c_char_p, ctypes.POINTER(SA_CTL_RequestID_t), SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "pkey", "value", "rID", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_RequestWritePropertyArray_i32(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int32) values, ctypes.c_size_t arraySize, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_RequestWritePropertyArray_i32", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t, ctypes.POINTER(SA_CTL_RequestID_t), SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "pkey", "values", "arraySize", "rID", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_RequestWritePropertyArray_i64(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_PropertyKey_t pkey, ctypes.POINTER(ctypes.c_int64) values, ctypes.c_size_t arraySize, ctypes.POINTER(SA_CTL_RequestID_t) rID, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_RequestWritePropertyArray_i64", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_PropertyKey_t, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t, ctypes.POINTER(SA_CTL_RequestID_t), SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "pkey", "values", "arraySize", "rID", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_WaitForWrite(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID)
    addfunc(lib, "SA_CTL_WaitForWrite", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_RequestID_t],
            argnames = ["dHandle", "rID"] )
    #  SA_CTL_Result_t SA_CTL_CancelRequest(SA_CTL_DeviceHandle_t dHandle, SA_CTL_RequestID_t rID)
    addfunc(lib, "SA_CTL_CancelRequest", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_RequestID_t],
            argnames = ["dHandle", "rID"] )
    #  SA_CTL_Result_t SA_CTL_CreateOutputBuffer(SA_CTL_DeviceHandle_t dHandle, ctypes.POINTER(SA_CTL_TransmitHandle_t) tHandle)
    addfunc(lib, "SA_CTL_CreateOutputBuffer", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.POINTER(SA_CTL_TransmitHandle_t)],
            argnames = ["dHandle", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_FlushOutputBuffer(SA_CTL_DeviceHandle_t dHandle, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_FlushOutputBuffer", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_CancelOutputBuffer(SA_CTL_DeviceHandle_t dHandle, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_CancelOutputBuffer", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_OpenCommandGroup(SA_CTL_DeviceHandle_t dHandle, ctypes.POINTER(SA_CTL_TransmitHandle_t) tHandle, ctypes.c_uint32 triggerMode)
    addfunc(lib, "SA_CTL_OpenCommandGroup", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.POINTER(SA_CTL_TransmitHandle_t), ctypes.c_uint32],
            argnames = ["dHandle", "tHandle", "triggerMode"] )
    #  SA_CTL_Result_t SA_CTL_CloseCommandGroup(SA_CTL_DeviceHandle_t dHandle, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_CloseCommandGroup", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_CancelCommandGroup(SA_CTL_DeviceHandle_t dHandle, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_CancelCommandGroup", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_WaitForEvent(SA_CTL_DeviceHandle_t dHandle, ctypes.POINTER(SA_CTL_Event_t) event, ctypes.c_uint32 timeout)
    addfunc(lib, "SA_CTL_WaitForEvent", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.POINTER(SA_CTL_Event_t), ctypes.c_uint32],
            argnames = ["dHandle", "event", "timeout"] )
    #  SA_CTL_Result_t SA_CTL_Calibrate(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_Calibrate", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_Reference(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_Reference", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_Move(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, ctypes.c_int64 moveValue, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_Move", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, ctypes.c_int64, SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "moveValue", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_Stop(SA_CTL_DeviceHandle_t dHandle, ctypes.c_int8 idx, SA_CTL_TransmitHandle_t tHandle)
    addfunc(lib, "SA_CTL_Stop", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.c_int8, SA_CTL_TransmitHandle_t],
            argnames = ["dHandle", "idx", "tHandle"] )
    #  SA_CTL_Result_t SA_CTL_OpenStream(SA_CTL_DeviceHandle_t dHandle, ctypes.POINTER(SA_CTL_StreamHandle_t) sHandle, ctypes.c_uint32 triggerMode)
    addfunc(lib, "SA_CTL_OpenStream", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, ctypes.POINTER(SA_CTL_StreamHandle_t), ctypes.c_uint32],
            argnames = ["dHandle", "sHandle", "triggerMode"] )
    #  SA_CTL_Result_t SA_CTL_StreamFrame(SA_CTL_DeviceHandle_t dHandle, SA_CTL_StreamHandle_t sHandle, ctypes.POINTER(ctypes.c_uint8) frameData, ctypes.c_uint32 frameSize)
    addfunc(lib, "SA_CTL_StreamFrame", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_StreamHandle_t, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32],
            argnames = ["dHandle", "sHandle", "frameData", "frameSize"] )
    #  SA_CTL_Result_t SA_CTL_CloseStream(SA_CTL_DeviceHandle_t dHandle, SA_CTL_StreamHandle_t sHandle)
    addfunc(lib, "SA_CTL_CloseStream", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_StreamHandle_t],
            argnames = ["dHandle", "sHandle"] )
    #  SA_CTL_Result_t SA_CTL_AbortStream(SA_CTL_DeviceHandle_t dHandle, SA_CTL_StreamHandle_t sHandle)
    addfunc(lib, "SA_CTL_AbortStream", restype = SA_CTL_Result_t,
            argtypes = [SA_CTL_DeviceHandle_t, SA_CTL_StreamHandle_t],
            argnames = ["dHandle", "sHandle"] )


