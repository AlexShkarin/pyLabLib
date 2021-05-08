##########   This file is generated automatically based on sc2_SDKStructures.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class PCO_INTERFACE(enum.IntEnum):
    PCO_INTERFACE_FW      = _int32(1)
    PCO_INTERFACE_CL_MTX  = _int32(2)
    PCO_INTERFACE_CL_ME3  = _int32(3)
    PCO_INTERFACE_CL_NAT  = _int32(4)
    PCO_INTERFACE_GIGE    = _int32(5)
    PCO_INTERFACE_USB     = _int32(6)
    PCO_INTERFACE_CL_ME4  = _int32(7)
    PCO_INTERFACE_USB3    = _int32(8)
    PCO_INTERFACE_WLAN    = _int32(9)
    PCO_INTERFACE_CLHS    = _int32(11)
    PCO_LASTINTERFACE     = _int32(11)
    PCO_INTERFACE_CL_SER  = _int32(10)
    PCO_INTERFACE_GENERIC = _int32(20)
dPCO_INTERFACE={a.name:a.value for a in PCO_INTERFACE}
drPCO_INTERFACE={a.value:a.name for a in PCO_INTERFACE}


class LENSCONTROL(enum.IntEnum):
    LENSCONTROL_LENSTYPE_NONE         = _int32(0)
    LENSCONTROL_TYPE_BIRGER           = _int32(0x00B189E8)
    LENSCONTROL_STATUS_LA_CMD_DONE    = _int32(0x00000001)
    LENSCONTROL_STATUS_LENSPRESENT    = _int32(0x00000002)
    LENSCONTROL_STATUS_NOAPERTURE     = _int32(0x00000004)
    LENSCONTROL_STATUS_MANUALFOCUS    = _int32(0x00000008)
    LENSCONTROL_STATUS_WAITINGFORLENS = _int32(0x00000010)
    LENSCONTROL_IN_LENSVALUE_RELATIVE = _int32(0x00001000)
    LENSCONTROL_OUT_LENSHITSTOP       = _int32(0x00100000)
    LENSCONTROL_OUT_LENSWASCHANGED    = _int32(0x00200000)
    LENSCONTROL_OUT_ZOOMHASCHANGED    = _int32(0x00400000)
dLENSCONTROL={a.name:a.value for a in LENSCONTROL}
drLENSCONTROL={a.value:a.name for a in LENSCONTROL}





##### TYPE DEFINITIONS #####





##### FUNCTION DEFINITIONS #####


