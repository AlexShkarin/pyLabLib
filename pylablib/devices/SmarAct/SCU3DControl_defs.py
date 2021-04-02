##########   This file is generated automatically based on SCU3DControl.h   ##########


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class EConfiguration(enum.IntEnum):
    SA_SYNCHRONOUS_COMMUNICATION  = _int32(0)
    SA_ASYNCHRONOUS_COMMUNICATION = _int32(1)
    SA_HARDWARE_RESET             = _int32(2)
dEConfiguration={a.name:a.value for a in EConfiguration}
drEConfiguration={a.value:a.name for a in EConfiguration}


class EReport(enum.IntEnum):
    SA_NO_REPORT_ON_COMPLETE = _int32(0)
    SA_REPORT_ON_COMPLETE    = _int32(1)
dEReport={a.name:a.value for a in EReport}
drEReport={a.value:a.name for a in EReport}


class Error(enum.IntEnum):
    SA_OK                             = _int32(0)
    SA_INITIALIZATION_ERROR           = _int32(1)
    SA_NOT_INITIALIZED_ERROR          = _int32(2)
    SA_NO_DEVICES_FOUND_ERROR         = _int32(3)
    SA_TOO_MANY_DEVICES_ERROR         = _int32(4)
    SA_INVALID_DEVICE_INDEX_ERROR     = _int32(5)
    SA_INVALID_CHANNEL_INDEX_ERROR    = _int32(6)
    SA_TRANSMIT_ERROR                 = _int32(7)
    SA_WRITE_ERROR                    = _int32(8)
    SA_INVALID_PARAMETER_ERROR        = _int32(9)
    SA_READ_ERROR                     = _int32(10)
    SA_INTERNAL_ERROR                 = _int32(12)
    SA_WRONG_MODE_ERROR               = _int32(13)
    SA_PROTOCOL_ERROR                 = _int32(14)
    SA_TIMEOUT_ERROR                  = _int32(15)
    SA_NOTIFICATION_ALREADY_SET_ERROR = _int32(16)
    SA_ID_LIST_TOO_SMALL_ERROR        = _int32(17)
    SA_DEVICE_ALREADY_ADDED_ERROR     = _int32(18)
    SA_DEVICE_NOT_FOUND_ERROR         = _int32(19)
    SA_INVALID_COMMAND_ERROR          = _int32(128)
    SA_COMMAND_NOT_SUPPORTED_ERROR    = _int32(129)
    SA_NO_SENSOR_PRESENT_ERROR        = _int32(130)
    SA_WRONG_SENSOR_TYPE_ERROR        = _int32(131)
    SA_END_STOP_REACHED_ERROR         = _int32(132)
    SA_COMMAND_OVERRIDDEN_ERROR       = _int32(133)
    SA_OTHER_ERROR                    = _int32(255)
dError={a.name:a.value for a in Error}
drError={a.value:a.name for a in Error}


class EPacketType(enum.IntEnum):
    SA_NO_PACKET_TYPE                      = _int32(0)
    SA_ERROR_PACKET_TYPE                   = _int32(1)
    SA_POSITION_PACKET_TYPE                = _int32(2)
    SA_ANGLE_PACKET_TYPE                   = _int32(3)
    SA_COMPLETED_PACKET_TYPE               = _int32(4)
    SA_STATUS_PACKET_TYPE                  = _int32(5)
    SA_CLOSED_LOOP_FREQUENCY_PACKET_TYPE   = _int32(6)
    SA_SENSOR_TYPE_PACKET_TYPE             = _int32(7)
    SA_SENSOR_PRESENT_PACKET_TYPE          = _int32(8)
    SA_AMPLITUDE_PACKET_TYPE               = _int32(9)
    SA_POSITIONER_ALIGNMENT_PACKET_TYPE    = _int32(10)
    SA_SAFE_DIRECTION_PACKET_TYPE          = _int32(11)
    SA_SCALE_PACKET_TYPE                   = _int32(12)
    SA_PHYSICAL_POSITION_KNOWN_PACKET_TYPE = _int32(13)
    SA_INVALID_PACKET_TYPE                 = _int32(255)
dEPacketType={a.name:a.value for a in EPacketType}
drEPacketType={a.value:a.name for a in EPacketType}


class EStatusCode(enum.IntEnum):
    SA_STOPPED_STATUS             = _int32(0)
    SA_SETTING_AMPLITUDE_STATUS   = _int32(1)
    SA_MOVING_STATUS              = _int32(2)
    SA_TARGETING_STATUS           = _int32(3)
    SA_HOLDING_STATUS             = _int32(4)
    SA_CALIBRATING_STATUS         = _int32(5)
    SA_MOVING_TO_REFERENCE_STATUS = _int32(6)
dEStatusCode={a.name:a.value for a in EStatusCode}
drEStatusCode={a.value:a.name for a in EStatusCode}


class ESensorType(enum.IntEnum):
    SA_M_SENSOR_TYPE      = _int32(1)
    SA_GA_SENSOR_TYPE     = _int32(2)
    SA_GB_SENSOR_TYPE     = _int32(3)
    SA_GC_SENSOR_TYPE     = _int32(4)
    SA_GD_SENSOR_TYPE     = _int32(5)
    SA_GE_SENSOR_TYPE     = _int32(6)
    SA_RA_SENSOR_TYPE     = _int32(7)
    SA_GF_SENSOR_TYPE     = _int32(8)
    SA_RB_SENSOR_TYPE     = _int32(9)
    SA_SR36M_SENSOR_TYPE  = _int32(10)
    SA_SR36ME_SENSOR_TYPE = _int32(11)
    SA_SR50M_SENSOR_TYPE  = _int32(12)
    SA_SR50ME_SENSOR_TYPE = _int32(13)
    SA_MM50_SENSOR_TYPE   = _int32(14)
    SA_G935M_SENSOR_TYPE  = _int32(15)
    SA_MD_SENSOR_TYPE     = _int32(16)
    SA_TT254_SENSOR_TYPE  = _int32(17)
dESensorType={a.name:a.value for a in ESensorType}
drESensorType={a.value:a.name for a in ESensorType}


class EAlignment(enum.IntEnum):
    SA_HORIZONTAL_ALIGNMENT = _int32(0)
    SA_VERTICAL_ALIGNMENT   = _int32(1)
dEAlignment={a.name:a.value for a in EAlignment}
drEAlignment={a.value:a.name for a in EAlignment}


class ECompatibility(enum.IntEnum):
    SA_NO_SENSOR_TYPE       = _int32(0)
    SA_L180_SENSOR_TYPE     = _int32(1)
    SA_G180R435_SENSOR_TYPE = _int32(2)
    SA_G180R560_SENSOR_TYPE = _int32(3)
    SA_G50R85_SENSOR_TYPE   = _int32(4)
dECompatibility={a.name:a.value for a in ECompatibility}
drECompatibility={a.value:a.name for a in ECompatibility}





##### TYPE DEFINITIONS #####


BYTE=ctypes.c_ubyte
PBYTE=ctypes.POINTER(BYTE)
CHAR=ctypes.c_char
PCHAR=ctypes.POINTER(CHAR)
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
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
HWND=ctypes.c_void_p
SA_STATUS=ctypes.c_uint
SA_INDEX=ctypes.c_uint
SA_PACKET_TYPE=ctypes.c_uint
class SA_PACKET(ctypes.Structure):
    _fields_=[  ("packetType",SA_PACKET_TYPE),
                ("channelIndex",SA_INDEX),
                ("data1",ctypes.c_uint),
                ("data2",ctypes.c_int),
                ("data3",ctypes.c_int) ]
PSA_PACKET=ctypes.POINTER(SA_PACKET)
class CSA_PACKET(ctypes_wrap.CStructWrapper):
    _struct=SA_PACKET





##### FUNCTION DEFINITIONS #####





def define_functions(lib):
    #  SA_STATUS SA_GetDLLVersion(ctypes.POINTER(ctypes.c_uint) version)
    lib.SA_GetDLLVersion.restype=SA_STATUS
    lib.SA_GetDLLVersion.argtypes=[ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetDLLVersion.argnames=["version"]
    #  SA_STATUS SA_GetAvailableDevices(ctypes.POINTER(ctypes.c_uint) idList, ctypes.POINTER(ctypes.c_uint) idListSize)
    lib.SA_GetAvailableDevices.restype=SA_STATUS
    lib.SA_GetAvailableDevices.argtypes=[ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetAvailableDevices.argnames=["idList", "idListSize"]
    #  SA_STATUS SA_AddDeviceToInitDevicesList(ctypes.c_uint deviceId)
    lib.SA_AddDeviceToInitDevicesList.restype=SA_STATUS
    lib.SA_AddDeviceToInitDevicesList.argtypes=[ctypes.c_uint]
    lib.SA_AddDeviceToInitDevicesList.argnames=["deviceId"]
    #  SA_STATUS SA_ClearInitDevicesList()
    lib.SA_ClearInitDevicesList.restype=SA_STATUS
    lib.SA_ClearInitDevicesList.argtypes=[]
    lib.SA_ClearInitDevicesList.argnames=[]
    #  SA_STATUS SA_InitDevices(ctypes.c_uint configuration)
    lib.SA_InitDevices.restype=SA_STATUS
    lib.SA_InitDevices.argtypes=[ctypes.c_uint]
    lib.SA_InitDevices.argnames=["configuration"]
    #  SA_STATUS SA_ReleaseDevices()
    lib.SA_ReleaseDevices.restype=SA_STATUS
    lib.SA_ReleaseDevices.argtypes=[]
    lib.SA_ReleaseDevices.argnames=[]
    #  SA_STATUS SA_GetNumberOfDevices(ctypes.POINTER(ctypes.c_uint) number)
    lib.SA_GetNumberOfDevices.restype=SA_STATUS
    lib.SA_GetNumberOfDevices.argtypes=[ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetNumberOfDevices.argnames=["number"]
    #  SA_STATUS SA_GetDeviceID(SA_INDEX deviceIndex, ctypes.POINTER(ctypes.c_uint) deviceId)
    lib.SA_GetDeviceID.restype=SA_STATUS
    lib.SA_GetDeviceID.argtypes=[SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetDeviceID.argnames=["deviceIndex", "deviceId"]
    #  SA_STATUS SA_GetDeviceFirmwareVersion(SA_INDEX deviceIndex, ctypes.POINTER(ctypes.c_uint) version)
    lib.SA_GetDeviceFirmwareVersion.restype=SA_STATUS
    lib.SA_GetDeviceFirmwareVersion.argtypes=[SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetDeviceFirmwareVersion.argnames=["deviceIndex", "version"]
    #  SA_STATUS SA_SetClosedLoopMaxFrequency_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint frequency)
    lib.SA_SetClosedLoopMaxFrequency_S.restype=SA_STATUS
    lib.SA_SetClosedLoopMaxFrequency_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetClosedLoopMaxFrequency_S.argnames=["deviceIndex", "channelIndex", "frequency"]
    #  SA_STATUS SA_GetClosedLoopMaxFrequency_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) frequency)
    lib.SA_GetClosedLoopMaxFrequency_S.restype=SA_STATUS
    lib.SA_GetClosedLoopMaxFrequency_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetClosedLoopMaxFrequency_S.argnames=["deviceIndex", "channelIndex", "frequency"]
    #  SA_STATUS SA_SetZero_S(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_SetZero_S.restype=SA_STATUS
    lib.SA_SetZero_S.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_SetZero_S.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_GetSensorPresent_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) present)
    lib.SA_GetSensorPresent_S.restype=SA_STATUS
    lib.SA_GetSensorPresent_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetSensorPresent_S.argnames=["deviceIndex", "channelIndex", "present"]
    #  SA_STATUS SA_SetSensorType_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint type)
    lib.SA_SetSensorType_S.restype=SA_STATUS
    lib.SA_SetSensorType_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetSensorType_S.argnames=["deviceIndex", "channelIndex", "type"]
    #  SA_STATUS SA_GetSensorType_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) type)
    lib.SA_GetSensorType_S.restype=SA_STATUS
    lib.SA_GetSensorType_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetSensorType_S.argnames=["deviceIndex", "channelIndex", "type"]
    #  SA_STATUS SA_SetPositionerAlignment_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint alignment, ctypes.c_uint forwardAmplitude, ctypes.c_uint backwardAmplitude)
    lib.SA_SetPositionerAlignment_S.restype=SA_STATUS
    lib.SA_SetPositionerAlignment_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    lib.SA_SetPositionerAlignment_S.argnames=["deviceIndex", "channelIndex", "alignment", "forwardAmplitude", "backwardAmplitude"]
    #  SA_STATUS SA_GetPositionerAlignment_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) alignment, ctypes.POINTER(ctypes.c_uint) forwardAmplitude, ctypes.POINTER(ctypes.c_uint) backwardAmplitude)
    lib.SA_GetPositionerAlignment_S.restype=SA_STATUS
    lib.SA_GetPositionerAlignment_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetPositionerAlignment_S.argnames=["deviceIndex", "channelIndex", "alignment", "forwardAmplitude", "backwardAmplitude"]
    #  SA_STATUS SA_SetSafeDirection_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint direction)
    lib.SA_SetSafeDirection_S.restype=SA_STATUS
    lib.SA_SetSafeDirection_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetSafeDirection_S.argnames=["deviceIndex", "channelIndex", "direction"]
    #  SA_STATUS SA_GetSafeDirection_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) direction)
    lib.SA_GetSafeDirection_S.restype=SA_STATUS
    lib.SA_GetSafeDirection_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetSafeDirection_S.argnames=["deviceIndex", "channelIndex", "direction"]
    #  SA_STATUS SA_SetScale_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int reserved, ctypes.c_uint inverted)
    lib.SA_SetScale_S.restype=SA_STATUS
    lib.SA_SetScale_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_uint]
    lib.SA_SetScale_S.argnames=["deviceIndex", "channelIndex", "reserved", "inverted"]
    #  SA_STATUS SA_GetScale_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_int) reserved, ctypes.POINTER(ctypes.c_uint) inverted)
    lib.SA_GetScale_S.restype=SA_STATUS
    lib.SA_GetScale_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetScale_S.argnames=["deviceIndex", "channelIndex", "reserved", "inverted"]
    #  SA_STATUS SA_MoveStep_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int steps, ctypes.c_uint amplitude, ctypes.c_uint frequency)
    lib.SA_MoveStep_S.restype=SA_STATUS
    lib.SA_MoveStep_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_uint, ctypes.c_uint]
    lib.SA_MoveStep_S.argnames=["deviceIndex", "channelIndex", "steps", "amplitude", "frequency"]
    #  SA_STATUS SA_SetAmplitude_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint amplitude)
    lib.SA_SetAmplitude_S.restype=SA_STATUS
    lib.SA_SetAmplitude_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetAmplitude_S.argnames=["deviceIndex", "channelIndex", "amplitude"]
    #  SA_STATUS SA_MovePositionAbsolute_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int position, ctypes.c_uint holdTime)
    lib.SA_MovePositionAbsolute_S.restype=SA_STATUS
    lib.SA_MovePositionAbsolute_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_uint]
    lib.SA_MovePositionAbsolute_S.argnames=["deviceIndex", "channelIndex", "position", "holdTime"]
    #  SA_STATUS SA_MovePositionRelative_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int diff, ctypes.c_uint holdTime)
    lib.SA_MovePositionRelative_S.restype=SA_STATUS
    lib.SA_MovePositionRelative_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_uint]
    lib.SA_MovePositionRelative_S.argnames=["deviceIndex", "channelIndex", "diff", "holdTime"]
    #  SA_STATUS SA_MoveAngleAbsolute_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int angle, ctypes.c_int revolution, ctypes.c_uint holdTime)
    lib.SA_MoveAngleAbsolute_S.restype=SA_STATUS
    lib.SA_MoveAngleAbsolute_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
    lib.SA_MoveAngleAbsolute_S.argnames=["deviceIndex", "channelIndex", "angle", "revolution", "holdTime"]
    #  SA_STATUS SA_MoveAngleRelative_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int angleDiff, ctypes.c_int revolutionDiff, ctypes.c_uint holdTime)
    lib.SA_MoveAngleRelative_S.restype=SA_STATUS
    lib.SA_MoveAngleRelative_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
    lib.SA_MoveAngleRelative_S.argnames=["deviceIndex", "channelIndex", "angleDiff", "revolutionDiff", "holdTime"]
    #  SA_STATUS SA_CalibrateSensor_S(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_CalibrateSensor_S.restype=SA_STATUS
    lib.SA_CalibrateSensor_S.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_CalibrateSensor_S.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_MoveToReference_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint holdTime, ctypes.c_uint autoZero)
    lib.SA_MoveToReference_S.restype=SA_STATUS
    lib.SA_MoveToReference_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint, ctypes.c_uint]
    lib.SA_MoveToReference_S.argnames=["deviceIndex", "channelIndex", "holdTime", "autoZero"]
    #  SA_STATUS SA_MoveToEndStop_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint direction, ctypes.c_uint holdTime, ctypes.c_uint autoZero)
    lib.SA_MoveToEndStop_S.restype=SA_STATUS
    lib.SA_MoveToEndStop_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    lib.SA_MoveToEndStop_S.argnames=["deviceIndex", "channelIndex", "direction", "holdTime", "autoZero"]
    #  SA_STATUS SA_Stop_S(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_Stop_S.restype=SA_STATUS
    lib.SA_Stop_S.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_Stop_S.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_GetStatus_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) status)
    lib.SA_GetStatus_S.restype=SA_STATUS
    lib.SA_GetStatus_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetStatus_S.argnames=["deviceIndex", "channelIndex", "status"]
    #  SA_STATUS SA_GetAmplitude_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) amplitude)
    lib.SA_GetAmplitude_S.restype=SA_STATUS
    lib.SA_GetAmplitude_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetAmplitude_S.argnames=["deviceIndex", "channelIndex", "amplitude"]
    #  SA_STATUS SA_GetPosition_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_int) position)
    lib.SA_GetPosition_S.restype=SA_STATUS
    lib.SA_GetPosition_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_int)]
    lib.SA_GetPosition_S.argnames=["deviceIndex", "channelIndex", "position"]
    #  SA_STATUS SA_GetAngle_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_int) angle, ctypes.POINTER(ctypes.c_int) revolution)
    lib.SA_GetAngle_S.restype=SA_STATUS
    lib.SA_GetAngle_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    lib.SA_GetAngle_S.argnames=["deviceIndex", "channelIndex", "angle", "revolution"]
    #  SA_STATUS SA_GetPhysicalPositionKnown_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.POINTER(ctypes.c_uint) known)
    lib.SA_GetPhysicalPositionKnown_S.restype=SA_STATUS
    lib.SA_GetPhysicalPositionKnown_S.argtypes=[SA_INDEX, SA_INDEX, ctypes.POINTER(ctypes.c_uint)]
    lib.SA_GetPhysicalPositionKnown_S.argnames=["deviceIndex", "channelIndex", "known"]
    #  SA_STATUS SA_SetClosedLoopMaxFrequency_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint frequency)
    lib.SA_SetClosedLoopMaxFrequency_A.restype=SA_STATUS
    lib.SA_SetClosedLoopMaxFrequency_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetClosedLoopMaxFrequency_A.argnames=["deviceIndex", "channelIndex", "frequency"]
    #  SA_STATUS SA_GetClosedLoopMaxFrequency_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetClosedLoopMaxFrequency_A.restype=SA_STATUS
    lib.SA_GetClosedLoopMaxFrequency_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetClosedLoopMaxFrequency_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_SetZero_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_SetZero_A.restype=SA_STATUS
    lib.SA_SetZero_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_SetZero_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_GetSensorPresent_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetSensorPresent_A.restype=SA_STATUS
    lib.SA_GetSensorPresent_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetSensorPresent_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_SetSensorType_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint type)
    lib.SA_SetSensorType_A.restype=SA_STATUS
    lib.SA_SetSensorType_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetSensorType_A.argnames=["deviceIndex", "channelIndex", "type"]
    #  SA_STATUS SA_GetSensorType_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetSensorType_A.restype=SA_STATUS
    lib.SA_GetSensorType_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetSensorType_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_SetPositionerAlignment_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint alignment, ctypes.c_uint forwardAmplitude, ctypes.c_uint backwardAmplitude)
    lib.SA_SetPositionerAlignment_A.restype=SA_STATUS
    lib.SA_SetPositionerAlignment_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    lib.SA_SetPositionerAlignment_A.argnames=["deviceIndex", "channelIndex", "alignment", "forwardAmplitude", "backwardAmplitude"]
    #  SA_STATUS SA_GetPositionerAlignment_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetPositionerAlignment_A.restype=SA_STATUS
    lib.SA_GetPositionerAlignment_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetPositionerAlignment_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_SetSafeDirection_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint direction)
    lib.SA_SetSafeDirection_A.restype=SA_STATUS
    lib.SA_SetSafeDirection_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetSafeDirection_A.argnames=["deviceIndex", "channelIndex", "direction"]
    #  SA_STATUS SA_GetSafeDirection_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetSafeDirection_A.restype=SA_STATUS
    lib.SA_GetSafeDirection_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetSafeDirection_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_SetScale_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int reserved, ctypes.c_uint inverted)
    lib.SA_SetScale_A.restype=SA_STATUS
    lib.SA_SetScale_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_uint]
    lib.SA_SetScale_A.argnames=["deviceIndex", "channelIndex", "reserved", "inverted"]
    #  SA_STATUS SA_GetScale_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetScale_A.restype=SA_STATUS
    lib.SA_GetScale_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetScale_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_SetReportOnComplete_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint report)
    lib.SA_SetReportOnComplete_A.restype=SA_STATUS
    lib.SA_SetReportOnComplete_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetReportOnComplete_A.argnames=["deviceIndex", "channelIndex", "report"]
    #  SA_STATUS SA_MoveStep_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int steps, ctypes.c_uint amplitude, ctypes.c_uint frequency)
    lib.SA_MoveStep_A.restype=SA_STATUS
    lib.SA_MoveStep_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_uint, ctypes.c_uint]
    lib.SA_MoveStep_A.argnames=["deviceIndex", "channelIndex", "steps", "amplitude", "frequency"]
    #  SA_STATUS SA_SetAmplitude_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint amplitude)
    lib.SA_SetAmplitude_A.restype=SA_STATUS
    lib.SA_SetAmplitude_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint]
    lib.SA_SetAmplitude_A.argnames=["deviceIndex", "channelIndex", "amplitude"]
    #  SA_STATUS SA_MovePositionAbsolute_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int position, ctypes.c_uint holdTime)
    lib.SA_MovePositionAbsolute_A.restype=SA_STATUS
    lib.SA_MovePositionAbsolute_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_uint]
    lib.SA_MovePositionAbsolute_A.argnames=["deviceIndex", "channelIndex", "position", "holdTime"]
    #  SA_STATUS SA_MovePositionRelative_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int diff, ctypes.c_uint holdTime)
    lib.SA_MovePositionRelative_A.restype=SA_STATUS
    lib.SA_MovePositionRelative_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_uint]
    lib.SA_MovePositionRelative_A.argnames=["deviceIndex", "channelIndex", "diff", "holdTime"]
    #  SA_STATUS SA_MoveAngleAbsolute_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int angle, ctypes.c_int revolution, ctypes.c_uint holdTime)
    lib.SA_MoveAngleAbsolute_A.restype=SA_STATUS
    lib.SA_MoveAngleAbsolute_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
    lib.SA_MoveAngleAbsolute_A.argnames=["deviceIndex", "channelIndex", "angle", "revolution", "holdTime"]
    #  SA_STATUS SA_MoveAngleRelative_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_int angleDiff, ctypes.c_int revolutionDiff, ctypes.c_uint holdTime)
    lib.SA_MoveAngleRelative_A.restype=SA_STATUS
    lib.SA_MoveAngleRelative_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
    lib.SA_MoveAngleRelative_A.argnames=["deviceIndex", "channelIndex", "angleDiff", "revolutionDiff", "holdTime"]
    #  SA_STATUS SA_CalibrateSensor_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_CalibrateSensor_A.restype=SA_STATUS
    lib.SA_CalibrateSensor_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_CalibrateSensor_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_MoveToReference_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint holdTime, ctypes.c_uint autoZero)
    lib.SA_MoveToReference_A.restype=SA_STATUS
    lib.SA_MoveToReference_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint, ctypes.c_uint]
    lib.SA_MoveToReference_A.argnames=["deviceIndex", "channelIndex", "holdTime", "autoZero"]
    #  SA_STATUS SA_MoveToEndStop_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint direction, ctypes.c_uint holdTime, ctypes.c_uint autoZero)
    lib.SA_MoveToEndStop_A.restype=SA_STATUS
    lib.SA_MoveToEndStop_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
    lib.SA_MoveToEndStop_A.argnames=["deviceIndex", "channelIndex", "direction", "holdTime", "autoZero"]
    #  SA_STATUS SA_Stop_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_Stop_A.restype=SA_STATUS
    lib.SA_Stop_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_Stop_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_GetStatus_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetStatus_A.restype=SA_STATUS
    lib.SA_GetStatus_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetStatus_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_GetAmplitude_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetAmplitude_A.restype=SA_STATUS
    lib.SA_GetAmplitude_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetAmplitude_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_GetPosition_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetPosition_A.restype=SA_STATUS
    lib.SA_GetPosition_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetPosition_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_GetAngle_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetAngle_A.restype=SA_STATUS
    lib.SA_GetAngle_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetAngle_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_GetPhysicalPositionKnown_A(SA_INDEX deviceIndex, SA_INDEX channelIndex)
    lib.SA_GetPhysicalPositionKnown_A.restype=SA_STATUS
    lib.SA_GetPhysicalPositionKnown_A.argtypes=[SA_INDEX, SA_INDEX]
    lib.SA_GetPhysicalPositionKnown_A.argnames=["deviceIndex", "channelIndex"]
    #  SA_STATUS SA_SetReceiveNotification_A(SA_INDEX deviceIndex, HANDLE event)
    lib.SA_SetReceiveNotification_A.restype=SA_STATUS
    lib.SA_SetReceiveNotification_A.argtypes=[SA_INDEX, HANDLE]
    lib.SA_SetReceiveNotification_A.argnames=["deviceIndex", "event"]
    #  SA_STATUS SA_ReceiveNextPacket_A(SA_INDEX deviceIndex, ctypes.c_uint timeout, ctypes.POINTER(SA_PACKET) packet)
    lib.SA_ReceiveNextPacket_A.restype=SA_STATUS
    lib.SA_ReceiveNextPacket_A.argtypes=[SA_INDEX, ctypes.c_uint, ctypes.POINTER(SA_PACKET)]
    lib.SA_ReceiveNextPacket_A.argnames=["deviceIndex", "timeout", "packet"]
    #  SA_STATUS SA_ReceiveNextPacketIfChannel_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, ctypes.c_uint timeout, ctypes.POINTER(SA_PACKET) packet)
    lib.SA_ReceiveNextPacketIfChannel_A.restype=SA_STATUS
    lib.SA_ReceiveNextPacketIfChannel_A.argtypes=[SA_INDEX, SA_INDEX, ctypes.c_uint, ctypes.POINTER(SA_PACKET)]
    lib.SA_ReceiveNextPacketIfChannel_A.argnames=["deviceIndex", "channelIndex", "timeout", "packet"]
    #  SA_STATUS SA_LookAtNextPacket_A(SA_INDEX deviceIndex, ctypes.c_uint timeout, ctypes.POINTER(SA_PACKET) packet)
    lib.SA_LookAtNextPacket_A.restype=SA_STATUS
    lib.SA_LookAtNextPacket_A.argtypes=[SA_INDEX, ctypes.c_uint, ctypes.POINTER(SA_PACKET)]
    lib.SA_LookAtNextPacket_A.argnames=["deviceIndex", "timeout", "packet"]
    #  SA_STATUS SA_DiscardPacket_A(SA_INDEX deviceIndex)
    lib.SA_DiscardPacket_A.restype=SA_STATUS
    lib.SA_DiscardPacket_A.argtypes=[SA_INDEX]
    lib.SA_DiscardPacket_A.argnames=["deviceIndex"]


