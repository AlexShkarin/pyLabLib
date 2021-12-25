##########   This file is generated automatically based on wlmData.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class EInst(enum.IntEnum):
    cInstCheckForWLM     = _int32(-1)
    cInstResetCalc       = _int32(0)
    cInstReturnMode      = _int32(0)
    cInstNotification    = _int32(1)
    cInstCopyPattern     = _int32(2)
    cInstCopyAnalysis    = _int32(2)
    cInstControlWLM      = _int32(3)
    cInstControlDelay    = _int32(4)
    cInstControlPriority = _int32(5)
dEInst={a.name:a.value for a in EInst}
drEInst={a.value:a.name for a in EInst}


class ENotify(enum.IntEnum):
    cNotifyInstallCallback    = _int32(0)
    cNotifyRemoveCallback     = _int32(1)
    cNotifyInstallWaitEvent   = _int32(2)
    cNotifyRemoveWaitEvent    = _int32(3)
    cNotifyInstallCallbackEx  = _int32(4)
    cNotifyInstallWaitEventEx = _int32(5)
dENotify={a.name:a.value for a in ENotify}
drENotify={a.value:a.name for a in ENotify}


class ESetError(enum.IntEnum):
    ResERR_NoErr                          = _int32(0)
    ResERR_WlmMissing                     = _int32(-1)
    ResERR_CouldNotSet                    = _int32(-2)
    ResERR_ParmOutOfRange                 = _int32(-3)
    ResERR_WlmOutOfResources              = _int32(-4)
    ResERR_WlmInternalError               = _int32(-5)
    ResERR_NotAvailable                   = _int32(-6)
    ResERR_WlmBusy                        = _int32(-7)
    ResERR_NotInMeasurementMode           = _int32(-8)
    ResERR_OnlyInMeasurementMode          = _int32(-9)
    ResERR_ChannelNotAvailable            = _int32(-10)
    ResERR_ChannelTemporarilyNotAvailable = _int32(-11)
    ResERR_CalOptionNotAvailable          = _int32(-12)
    ResERR_CalWavelengthOutOfRange        = _int32(-13)
    ResERR_BadCalibrationSignal           = _int32(-14)
    ResERR_UnitNotAvailable               = _int32(-15)
    ResERR_FileNotFound                   = _int32(-16)
    ResERR_FileCreation                   = _int32(-17)
    ResERR_TriggerPending                 = _int32(-18)
    ResERR_TriggerWaiting                 = _int32(-19)
    ResERR_NoLegitimation                 = _int32(-20)
dESetError={a.name:a.value for a in ESetError}
drESetError={a.value:a.name for a in ESetError}


class EEvent(enum.IntEnum):
    cmiResultMode                 = _int32(1)
    cmiRange                      = _int32(2)
    cmiPulse                      = _int32(3)
    cmiPulseMode                  = _int32(3)
    cmiWideLine                   = _int32(4)
    cmiWideMode                   = _int32(4)
    cmiFast                       = _int32(5)
    cmiFastMode                   = _int32(5)
    cmiExposureMode               = _int32(6)
    cmiExposureValue1             = _int32(7)
    cmiExposureValue2             = _int32(8)
    cmiDelay                      = _int32(9)
    cmiShift                      = _int32(10)
    cmiShift2                     = _int32(11)
    cmiReduce                     = _int32(12)
    cmiReduced                    = _int32(12)
    cmiScale                      = _int32(13)
    cmiTemperature                = _int32(14)
    cmiLink                       = _int32(15)
    cmiOperation                  = _int32(16)
    cmiDisplayMode                = _int32(17)
    cmiPattern1a                  = _int32(18)
    cmiPattern1b                  = _int32(19)
    cmiPattern2a                  = _int32(20)
    cmiPattern2b                  = _int32(21)
    cmiMin1                       = _int32(22)
    cmiMax1                       = _int32(23)
    cmiMin2                       = _int32(24)
    cmiMax2                       = _int32(25)
    cmiNowTick                    = _int32(26)
    cmiCallback                   = _int32(27)
    cmiFrequency1                 = _int32(28)
    cmiFrequency2                 = _int32(29)
    cmiDLLDetach                  = _int32(30)
    cmiVersion                    = _int32(31)
    cmiAnalysisMode               = _int32(32)
    cmiDeviationMode              = _int32(33)
    cmiDeviationReference         = _int32(34)
    cmiDeviationSensitivity       = _int32(35)
    cmiAppearance                 = _int32(36)
    cmiAutoCalMode                = _int32(37)
    cmiWavelength1                = _int32(42)
    cmiWavelength2                = _int32(43)
    cmiLinewidth                  = _int32(44)
    cmiLinewidthMode              = _int32(45)
    cmiLinkDlg                    = _int32(56)
    cmiAnalysis                   = _int32(57)
    cmiAnalogIn                   = _int32(66)
    cmiAnalogOut                  = _int32(67)
    cmiDistance                   = _int32(69)
    cmiWavelength3                = _int32(90)
    cmiWavelength4                = _int32(91)
    cmiWavelength5                = _int32(92)
    cmiWavelength6                = _int32(93)
    cmiWavelength7                = _int32(94)
    cmiWavelength8                = _int32(95)
    cmiVersion0                   = _int32(31)
    cmiVersion1                   = _int32(96)
    cmiDLLAttach                  = _int32(121)
    cmiSwitcherSignal             = _int32(123)
    cmiSwitcherMode               = _int32(124)
    cmiExposureValue11            = _int32(7)
    cmiExposureValue12            = _int32(125)
    cmiExposureValue13            = _int32(126)
    cmiExposureValue14            = _int32(127)
    cmiExposureValue15            = _int32(128)
    cmiExposureValue16            = _int32(129)
    cmiExposureValue17            = _int32(130)
    cmiExposureValue18            = _int32(131)
    cmiExposureValue21            = _int32(8)
    cmiExposureValue22            = _int32(132)
    cmiExposureValue23            = _int32(133)
    cmiExposureValue24            = _int32(134)
    cmiExposureValue25            = _int32(135)
    cmiExposureValue26            = _int32(136)
    cmiExposureValue27            = _int32(137)
    cmiExposureValue28            = _int32(138)
    cmiPatternAverage             = _int32(139)
    cmiPatternAvg1                = _int32(140)
    cmiPatternAvg2                = _int32(141)
    cmiAnalogOut1                 = _int32(67)
    cmiAnalogOut2                 = _int32(142)
    cmiMin11                      = _int32(22)
    cmiMin12                      = _int32(146)
    cmiMin13                      = _int32(147)
    cmiMin14                      = _int32(148)
    cmiMin15                      = _int32(149)
    cmiMin16                      = _int32(150)
    cmiMin17                      = _int32(151)
    cmiMin18                      = _int32(152)
    cmiMin21                      = _int32(24)
    cmiMin22                      = _int32(153)
    cmiMin23                      = _int32(154)
    cmiMin24                      = _int32(155)
    cmiMin25                      = _int32(156)
    cmiMin26                      = _int32(157)
    cmiMin27                      = _int32(158)
    cmiMin28                      = _int32(159)
    cmiMax11                      = _int32(23)
    cmiMax12                      = _int32(160)
    cmiMax13                      = _int32(161)
    cmiMax14                      = _int32(162)
    cmiMax15                      = _int32(163)
    cmiMax16                      = _int32(164)
    cmiMax17                      = _int32(165)
    cmiMax18                      = _int32(166)
    cmiMax21                      = _int32(25)
    cmiMax22                      = _int32(167)
    cmiMax23                      = _int32(168)
    cmiMax24                      = _int32(169)
    cmiMax25                      = _int32(170)
    cmiMax26                      = _int32(171)
    cmiMax27                      = _int32(172)
    cmiMax28                      = _int32(173)
    cmiAvg11                      = _int32(140)
    cmiAvg12                      = _int32(174)
    cmiAvg13                      = _int32(175)
    cmiAvg14                      = _int32(176)
    cmiAvg15                      = _int32(177)
    cmiAvg16                      = _int32(178)
    cmiAvg17                      = _int32(179)
    cmiAvg18                      = _int32(180)
    cmiAvg21                      = _int32(141)
    cmiAvg22                      = _int32(181)
    cmiAvg23                      = _int32(182)
    cmiAvg24                      = _int32(183)
    cmiAvg25                      = _int32(184)
    cmiAvg26                      = _int32(185)
    cmiAvg27                      = _int32(186)
    cmiAvg28                      = _int32(187)
    cmiPatternAnalysisWritten     = _int32(202)
    cmiSwitcherChannel            = _int32(203)
    cmiAnalogOut3                 = _int32(237)
    cmiAnalogOut4                 = _int32(238)
    cmiAnalogOut5                 = _int32(239)
    cmiAnalogOut6                 = _int32(240)
    cmiAnalogOut7                 = _int32(241)
    cmiAnalogOut8                 = _int32(242)
    cmiIntensity                  = _int32(251)
    cmiPower                      = _int32(267)
    cmiActiveChannel              = _int32(300)
    cmiPIDCourse                  = _int32(1030)
    cmiPIDUseTa                   = _int32(1031)
    cmiPIDUseT                    = _int32(1031)
    cmiPID_T                      = _int32(1033)
    cmiPID_P                      = _int32(1034)
    cmiPID_I                      = _int32(1035)
    cmiPID_D                      = _int32(1036)
    cmiDeviationSensitivityDim    = _int32(1040)
    cmiDeviationSensitivityFactor = _int32(1037)
    cmiDeviationPolarity          = _int32(1038)
    cmiDeviationSensitivityEx     = _int32(1039)
    cmiDeviationUnit              = _int32(1041)
    cmiDeviationBoundsMin         = _int32(1042)
    cmiDeviationBoundsMax         = _int32(1043)
    cmiDeviationRefMid            = _int32(1044)
    cmiDeviationRefAt             = _int32(1045)
    cmiPIDConstdt                 = _int32(1059)
    cmiPID_dt                     = _int32(1060)
    cmiPID_AutoClearHistory       = _int32(1061)
    cmiDeviationChannel           = _int32(1063)
    cmiAutoCalPeriod              = _int32(1120)
    cmiAutoCalUnit                = _int32(1121)
    cmiServerInitialized          = _int32(1124)
    cmiWavelength9                = _int32(1130)
    cmiExposureValue19            = _int32(1155)
    cmiExposureValue29            = _int32(1180)
    cmiMin19                      = _int32(1205)
    cmiMin29                      = _int32(1230)
    cmiMax19                      = _int32(1255)
    cmiMax29                      = _int32(1280)
    cmiAvg19                      = _int32(1305)
    cmiAvg29                      = _int32(1330)
    cmiWavelength10               = _int32(1355)
    cmiWavelength11               = _int32(1356)
    cmiWavelength12               = _int32(1357)
    cmiWavelength13               = _int32(1358)
    cmiWavelength14               = _int32(1359)
    cmiWavelength15               = _int32(1360)
    cmiWavelength16               = _int32(1361)
    cmiWavelength17               = _int32(1362)
    cmiExternalInput              = _int32(1400)
    cmiPressure                   = _int32(1465)
    cmiBackground                 = _int32(1475)
    cmiDistanceMode               = _int32(1476)
    cmiInterval                   = _int32(1477)
    cmiIntervalMode               = _int32(1478)
    cmiCalibrationEffect          = _int32(1480)
    cmiLinewidth1                 = _int32(44)
    cmiLinewidth2                 = _int32(1481)
    cmiLinewidth3                 = _int32(1482)
    cmiLinewidth4                 = _int32(1483)
    cmiLinewidth5                 = _int32(1484)
    cmiLinewidth6                 = _int32(1485)
    cmiLinewidth7                 = _int32(1486)
    cmiLinewidth8                 = _int32(1487)
    cmiLinewidth9                 = _int32(1488)
    cmiLinewidth10                = _int32(1489)
    cmiLinewidth11                = _int32(1490)
    cmiLinewidth12                = _int32(1491)
    cmiLinewidth13                = _int32(1492)
    cmiLinewidth14                = _int32(1493)
    cmiLinewidth15                = _int32(1494)
    cmiLinewidth16                = _int32(1495)
    cmiLinewidth17                = _int32(1496)
    cmiTriggerState               = _int32(1497)
    cmiDeviceAttach               = _int32(1501)
    cmiDeviceDetach               = _int32(1502)
dEEvent={a.name:a.value for a in EEvent}
drEEvent={a.value:a.name for a in EEvent}


class ECtrlMode(enum.IntEnum):
    cCtrlWLMShow        = _int32(1)
    cCtrlWLMHide        = _int32(2)
    cCtrlWLMExit        = _int32(3)
    cCtrlWLMStore       = _int32(4)
    cCtrlWLMCompare     = _int32(5)
    cCtrlWLMWait        = _int32(0x0010)
    cCtrlWLMStartSilent = _int32(0x0020)
    cCtrlWLMSilent      = _int32(0x0040)
    cCtrlWLMStartDelay  = _int32(0x0080)
dECtrlMode={a.name:a.value for a in ECtrlMode}
drECtrlMode={a.value:a.name for a in ECtrlMode}


class EOperation(enum.IntEnum):
    cStop        = _int32(0)
    cAdjustment  = _int32(1)
    cMeasurement = _int32(2)
dEOperation={a.name:a.value for a in EOperation}
drEOperation={a.value:a.name for a in EOperation}


class EBaseOperation(enum.IntEnum):
    cCtrlStopAll          = _int32(0)
    cCtrlStartAdjustment  = _int32(1)
    cCtrlStartMeasurement = _int32(2)
    cCtrlStartRecord      = _int32(0x0004)
    cCtrlStartReplay      = _int32(0x0008)
    cCtrlStoreArray       = _int32(0x0010)
    cCtrlLoadArray        = _int32(0x0020)
dEBaseOperation={a.name:a.value for a in EBaseOperation}
drEBaseOperation={a.value:a.name for a in EBaseOperation}


class EAddOperation(enum.IntEnum):
    cCtrlDontOverwrite = _int32(0x0000)
    cCtrlFileGiven     = _int32(0x0000)
dEAddOperation={a.name:a.value for a in EAddOperation}
drEAddOperation={a.value:a.name for a in EAddOperation}


class EMeasCtrl(enum.IntEnum):
    cCtrlMeasDelayRemove    = _int32(0)
    cCtrlMeasDelayGenerally = _int32(1)
    cCtrlMeasDelayOnce      = _int32(2)
    cCtrlMeasDelayDenyUntil = _int32(3)
    cCtrlMeasDelayIdleOnce  = _int32(4)
    cCtrlMeasDelayIdleEach  = _int32(5)
    cCtrlMeasDelayDefault   = _int32(6)
dEMeasCtrl={a.name:a.value for a in EMeasCtrl}
drEMeasCtrl={a.value:a.name for a in EMeasCtrl}


class ETriggerAction(enum.IntEnum):
    cCtrlMeasurementContinue       = _int32(0)
    cCtrlMeasurementInterrupt      = _int32(1)
    cCtrlMeasurementTriggerPoll    = _int32(2)
    cCtrlMeasurementTriggerSuccess = _int32(3)
    cCtrlMeasurementEx             = _int32(0x0100)
dETriggerAction={a.name:a.value for a in ETriggerAction}
drETriggerAction={a.value:a.name for a in ETriggerAction}


class EExpoRange(enum.IntEnum):
    cExpoMin  = _int32(0)
    cExpoMax  = _int32(1)
    cExpo2Min = _int32(2)
    cExpo2Max = _int32(3)
dEExpoRange={a.name:a.value for a in EExpoRange}
drEExpoRange={a.value:a.name for a in EExpoRange}


class EAmpConst(enum.IntEnum):
    cMin1 = _int32(0)
    cMin2 = _int32(1)
    cMax1 = _int32(2)
    cMax2 = _int32(3)
    cAvg1 = _int32(4)
    cAvg2 = _int32(5)
dEAmpConst={a.name:a.value for a in EAmpConst}
drEAmpConst={a.value:a.name for a in EAmpConst}


class EMeasRange(enum.IntEnum):
    cRange_250_410   = _int32(4)
    cRange_250_425   = _int32(0)
    cRange_300_410   = _int32(3)
    cRange_350_500   = _int32(5)
    cRange_400_725   = _int32(1)
    cRange_700_1100  = _int32(2)
    cRange_800_1300  = _int32(6)
    cRange_900_1500  = _int32(6)
    cRange_1100_1700 = _int32(7)
    cRange_1100_1800 = _int32(7)
dEMeasRange={a.name:a.value for a in EMeasRange}
drEMeasRange={a.value:a.name for a in EMeasRange}


class EMeasRangeMode(enum.IntEnum):
    cRangeModelOld          = _int32(65535)
    cRangeModelByOrder      = _int32(65534)
    cRangeModelByWavelength = _int32(65533)
dEMeasRangeMode={a.name:a.value for a in EMeasRangeMode}
drEMeasRangeMode={a.value:a.name for a in EMeasRangeMode}


class EMeasUnit(enum.IntEnum):
    cReturnWavelengthVac = _int32(0)
    cReturnWavelengthAir = _int32(1)
    cReturnFrequency     = _int32(2)
    cReturnWavenumber    = _int32(3)
    cReturnPhotonEnergy  = _int32(4)
dEMeasUnit={a.name:a.value for a in EMeasUnit}
drEMeasUnit={a.value:a.name for a in EMeasUnit}


class EPowerUnit(enum.IntEnum):
    cPower_muW = _int32(0)
    cPower_dBm = _int32(1)
dEPowerUnit={a.name:a.value for a in EPowerUnit}
drEPowerUnit={a.value:a.name for a in EPowerUnit}


class ECalibration(enum.IntEnum):
    cHeNe633  = _int32(0)
    cHeNe1152 = _int32(0)
    cNeL      = _int32(1)
    cOther    = _int32(2)
    cFreeHeNe = _int32(3)
dECalibration={a.name:a.value for a in ECalibration}
drECalibration={a.value:a.name for a in ECalibration}


class EAutocalibration(enum.IntEnum):
    cACOnceOnStart  = _int32(0)
    cACMeasurements = _int32(1)
    cACDays         = _int32(2)
    cACHours        = _int32(3)
    cACMinutes      = _int32(4)
dEAutocalibration={a.name:a.value for a in EAutocalibration}
drEAutocalibration={a.value:a.name for a in EAutocalibration}


class EExpRange(enum.IntEnum):
    cGetSync = _int32(1)
    cSetSync = _int32(2)
dEExpRange={a.name:a.value for a in EExpRange}
drEExpRange={a.value:a.name for a in EExpRange}


class ESignal(enum.IntEnum):
    cSignal1Interferometers    = _int32(0)
    cSignal1WideInterferometer = _int32(1)
    cSignal1Grating            = _int32(1)
    cSignal2Interferometers    = _int32(2)
    cSignal2WideInterferometer = _int32(3)
    cSignalAnalysis            = _int32(4)
    cSignalAnalysisX           = _int32(4)
    cSignalAnalysisY           = _int32(4 + 1)
dESignal={a.name:a.value for a in ESignal}
drESignal={a.value:a.name for a in ESignal}


class EGetError(enum.IntEnum):
    ErrNoValue              = _int32(0)
    ErrNoSignal             = _int32(-1)
    ErrBadSignal            = _int32(-2)
    ErrLowSignal            = _int32(-3)
    ErrBigSignal            = _int32(-4)
    ErrWlmMissing           = _int32(-5)
    ErrNotAvailable         = _int32(-6)
    InfNothingChanged       = _int32(-7)
    ErrNoPulse              = _int32(-8)
    ErrDiv0                 = _int32(-13)
    ErrOutOfRange           = _int32(-14)
    ErrUnitNotAvailable     = _int32(-15)
    ErrMaxErr               = _int32(-15)
    ErrTemperature          = _int32(-1000)
    ErrTempNotMeasured      = _int32(-1000 + 0)
    ErrTempNotAvailable     = _int32(-1000 + -6)
    ErrTempWlmMissing       = _int32(-1000 + -5)
    ErrDistance             = _int32(-1000000000)
    ErrDistanceNotAvailable = _int32(-1000000000 + -6)
    ErrDistanceWlmMissing   = _int32(-1000000000 + -5)
dEGetError={a.name:a.value for a in EGetError}
drEGetError={a.value:a.name for a in EGetError}


class EControlFlag(enum.IntEnum):
    flServerStarted           = _int32(0x00000001)
    flErrDeviceNotFound       = _int32(0x00000002)
    flErrDriverError          = _int32(0x00000004)
    flErrUSBError             = _int32(0x00000008)
    flErrUnknownDeviceError   = _int32(0x00000010)
    flErrWrongSN              = _int32(0x00000020)
    flErrUnknownSN            = _int32(0x00000040)
    flErrTemperatureError     = _int32(0x00000080)
    flErrPressureError        = _int32(0x00000100)
    flErrCancelledManually    = _int32(0x00000200)
    flErrWLMBusy              = _int32(0x00000400)
    flErrUnknownError         = _int32(0x00001000)
    flNoInstalledVersionFound = _int32(0x00002000)
    flDesiredVersionNotFound  = _int32(0x00004000)
    flErrFileNotFound         = _int32(0x00008000)
    flErrParmOutOfRange       = _int32(0x00010000)
    flErrCouldNotSet          = _int32(0x00020000)
    flErrEEPROMFailed         = _int32(0x00040000)
    flErrFileFailed           = _int32(0x00080000)
    flDeviceDataNewer         = _int32(0x00100000)
    flFileDataNewer           = _int32(0x00200000)
    flErrDeviceVersionOld     = _int32(0x00400000)
    flErrFileVersionOld       = _int32(0x00800000)
    flDeviceStampNewer        = _int32(0x01000000)
    flFileStampNewer          = _int32(0x02000000)
dEControlFlag={a.name:a.value for a in EControlFlag}
drEControlFlag={a.value:a.name for a in EControlFlag}


class EFileInfoFlag(enum.IntEnum):
    flFileInfoDoesntExist = _int32(0x0000)
    flFileInfoExists      = _int32(0x0001)
    flFileInfoCantWrite   = _int32(0x0002)
    flFileInfoCantRead    = _int32(0x0004)
    flFileInfoInvalidName = _int32(0x0008)
    cFileParameterError   = _int32(-1)
dEFileInfoFlag={a.name:a.value for a in EFileInfoFlag}
drEFileInfoFlag={a.value:a.name for a in EFileInfoFlag}





##### TYPE DEFINITIONS #####


BYTE=ctypes.c_ubyte
PBYTE=ctypes.POINTER(BYTE)
CHAR=ctypes.c_char
PCHAR=ctypes.c_char_p
UCHAR=ctypes.c_ubyte
PUCHAR=ctypes.POINTER(UCHAR)
ULONG_PTR=ctypes.c_uint64
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
lref=ctypes.POINTER(ctypes.c_long)
l64ref=ctypes.POINTER(ctypes.c_int64)
dref=ctypes.POINTER(ctypes.c_double)
sref=ctypes.c_char_p
bool=ctypes.c_long  # pylint: disable=redefined-builtin



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
    #  ctypes.c_int64 Instantiate(ctypes.c_long RFC, ctypes.c_long Mode, ctypes.c_int64 P1, ctypes.c_long P2)
    addfunc(lib, "Instantiate", restype = ctypes.c_int64,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_int64, ctypes.c_long],
            argnames = ["RFC", "Mode", "P1", "P2"] )
    #  ctypes.c_long WaitForWLMEvent(lref Mode, lref IntVal, dref DblVal)
    addfunc(lib, "WaitForWLMEvent", restype = ctypes.c_long,
            argtypes = [lref, lref, dref],
            argnames = ["Mode", "IntVal", "DblVal"] )
    #  ctypes.c_long WaitForWLMEventEx(lref Ver, lref Mode, lref IntVal, dref DblVal, lref Res1)
    addfunc(lib, "WaitForWLMEventEx", restype = ctypes.c_long,
            argtypes = [lref, lref, lref, dref, lref],
            argnames = ["Ver", "Mode", "IntVal", "DblVal", "Res1"] )
    #  ctypes.c_long WaitForNextWLMEvent(lref Mode, lref IntVal, dref DblVal)
    addfunc(lib, "WaitForNextWLMEvent", restype = ctypes.c_long,
            argtypes = [lref, lref, dref],
            argnames = ["Mode", "IntVal", "DblVal"] )
    #  ctypes.c_long WaitForNextWLMEventEx(lref Ver, lref Mode, lref IntVal, dref DblVal, lref Res1)
    addfunc(lib, "WaitForNextWLMEventEx", restype = ctypes.c_long,
            argtypes = [lref, lref, lref, dref, lref],
            argnames = ["Ver", "Mode", "IntVal", "DblVal", "Res1"] )
    #  None ClearWLMEvents()
    addfunc(lib, "ClearWLMEvents", restype = None,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_long ControlWLM(ctypes.c_long Action, ctypes.c_int64 App, ctypes.c_long Ver)
    addfunc(lib, "ControlWLM", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_int64, ctypes.c_long],
            argnames = ["Action", "App", "Ver"] )
    #  ctypes.c_long ControlWLMEx(ctypes.c_long Action, ctypes.c_int64 App, ctypes.c_long Ver, ctypes.c_long Delay, ctypes.c_long Res)
    addfunc(lib, "ControlWLMEx", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_int64, ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["Action", "App", "Ver", "Delay", "Res"] )
    #  ctypes.c_int64 SynchroniseWLM(ctypes.c_long Mode, ctypes.c_int64 TS)
    addfunc(lib, "SynchroniseWLM", restype = ctypes.c_int64,
            argtypes = [ctypes.c_long, ctypes.c_int64],
            argnames = ["Mode", "TS"] )
    #  ctypes.c_long SetMeasurementDelayMethod(ctypes.c_long Mode, ctypes.c_long Delay)
    addfunc(lib, "SetMeasurementDelayMethod", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long],
            argnames = ["Mode", "Delay"] )
    #  ctypes.c_long SetWLMPriority(ctypes.c_long PPC, ctypes.c_long Res1, ctypes.c_long Res2)
    addfunc(lib, "SetWLMPriority", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["PPC", "Res1", "Res2"] )
    #  ctypes.c_long PresetWLMIndex(ctypes.c_long Ver)
    addfunc(lib, "PresetWLMIndex", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Ver"] )
    #  ctypes.c_long GetWLMVersion(ctypes.c_long Ver)
    addfunc(lib, "GetWLMVersion", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Ver"] )
    #  ctypes.c_long GetWLMIndex(ctypes.c_long Ver)
    addfunc(lib, "GetWLMIndex", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Ver"] )
    #  ctypes.c_long GetWLMCount(ctypes.c_long V)
    addfunc(lib, "GetWLMCount", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["V"] )
    #  ctypes.c_double GetWavelength(ctypes.c_double WL)
    addfunc(lib, "GetWavelength", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["WL"] )
    #  ctypes.c_double GetWavelength2(ctypes.c_double WL2)
    addfunc(lib, "GetWavelength2", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["WL2"] )
    #  ctypes.c_double GetWavelengthNum(ctypes.c_long num, ctypes.c_double WL)
    addfunc(lib, "GetWavelengthNum", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["num", "WL"] )
    #  ctypes.c_double GetCalWavelength(ctypes.c_long ba, ctypes.c_double WL)
    addfunc(lib, "GetCalWavelength", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["ba", "WL"] )
    #  ctypes.c_double GetCalibrationEffect(ctypes.c_double CE)
    addfunc(lib, "GetCalibrationEffect", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["CE"] )
    #  ctypes.c_double GetFrequency(ctypes.c_double F)
    addfunc(lib, "GetFrequency", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["F"] )
    #  ctypes.c_double GetFrequency2(ctypes.c_double F2)
    addfunc(lib, "GetFrequency2", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["F2"] )
    #  ctypes.c_double GetFrequencyNum(ctypes.c_long num, ctypes.c_double F)
    addfunc(lib, "GetFrequencyNum", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["num", "F"] )
    #  ctypes.c_double GetLinewidth(ctypes.c_long Index, ctypes.c_double LW)
    addfunc(lib, "GetLinewidth", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["Index", "LW"] )
    #  ctypes.c_double GetLinewidthNum(ctypes.c_long num, ctypes.c_double LW)
    addfunc(lib, "GetLinewidthNum", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["num", "LW"] )
    #  ctypes.c_double GetDistance(ctypes.c_double D)
    addfunc(lib, "GetDistance", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["D"] )
    #  ctypes.c_double GetAnalogIn(ctypes.c_double AI)
    addfunc(lib, "GetAnalogIn", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["AI"] )
    #  ctypes.c_double GetTemperature(ctypes.c_double T)
    addfunc(lib, "GetTemperature", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["T"] )
    #  ctypes.c_long SetTemperature(ctypes.c_double T)
    addfunc(lib, "SetTemperature", restype = ctypes.c_long,
            argtypes = [ctypes.c_double],
            argnames = ["T"] )
    #  ctypes.c_double GetPressure(ctypes.c_double P)
    addfunc(lib, "GetPressure", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["P"] )
    #  ctypes.c_long SetPressure(ctypes.c_long Mode, ctypes.c_double P)
    addfunc(lib, "SetPressure", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["Mode", "P"] )
    #  ctypes.c_double GetExternalInput(ctypes.c_long Index, ctypes.c_double I)
    addfunc(lib, "GetExternalInput", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["Index", "I"] )
    #  ctypes.c_long SetExternalInput(ctypes.c_long Index, ctypes.c_double I)
    addfunc(lib, "SetExternalInput", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["Index", "I"] )
    #  ctypes.c_ushort GetExposure(ctypes.c_ushort E)
    addfunc(lib, "GetExposure", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["E"] )
    #  ctypes.c_long SetExposure(ctypes.c_ushort E)
    addfunc(lib, "SetExposure", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["E"] )
    #  ctypes.c_ushort GetExposure2(ctypes.c_ushort E2)
    addfunc(lib, "GetExposure2", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["E2"] )
    #  ctypes.c_long SetExposure2(ctypes.c_ushort E2)
    addfunc(lib, "SetExposure2", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["E2"] )
    #  ctypes.c_long GetExposureNum(ctypes.c_long num, ctypes.c_long arr, ctypes.c_long E)
    addfunc(lib, "GetExposureNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["num", "arr", "E"] )
    #  ctypes.c_long SetExposureNum(ctypes.c_long num, ctypes.c_long arr, ctypes.c_long E)
    addfunc(lib, "SetExposureNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["num", "arr", "E"] )
    #  bool GetExposureMode(bool EM)
    addfunc(lib, "GetExposureMode", restype = bool,
            argtypes = [bool],
            argnames = ["EM"] )
    #  ctypes.c_long SetExposureMode(bool EM)
    addfunc(lib, "SetExposureMode", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["EM"] )
    #  ctypes.c_long GetExposureModeNum(ctypes.c_long num, bool EM)
    addfunc(lib, "GetExposureModeNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, bool],
            argnames = ["num", "EM"] )
    #  ctypes.c_long SetExposureModeNum(ctypes.c_long num, bool EM)
    addfunc(lib, "SetExposureModeNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, bool],
            argnames = ["num", "EM"] )
    #  ctypes.c_long GetExposureRange(ctypes.c_long ER)
    addfunc(lib, "GetExposureRange", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["ER"] )
    #  ctypes.c_ushort GetResultMode(ctypes.c_ushort RM)
    addfunc(lib, "GetResultMode", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["RM"] )
    #  ctypes.c_long SetResultMode(ctypes.c_ushort RM)
    addfunc(lib, "SetResultMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["RM"] )
    #  ctypes.c_ushort GetRange(ctypes.c_ushort R)
    addfunc(lib, "GetRange", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["R"] )
    #  ctypes.c_long SetRange(ctypes.c_ushort R)
    addfunc(lib, "SetRange", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["R"] )
    #  ctypes.c_ushort GetPulseMode(ctypes.c_ushort PM)
    addfunc(lib, "GetPulseMode", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["PM"] )
    #  ctypes.c_long SetPulseMode(ctypes.c_ushort PM)
    addfunc(lib, "SetPulseMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["PM"] )
    #  ctypes.c_ushort GetWideMode(ctypes.c_ushort WM)
    addfunc(lib, "GetWideMode", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["WM"] )
    #  ctypes.c_long SetWideMode(ctypes.c_ushort WM)
    addfunc(lib, "SetWideMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["WM"] )
    #  ctypes.c_long GetDisplayMode(ctypes.c_long DM)
    addfunc(lib, "GetDisplayMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["DM"] )
    #  ctypes.c_long SetDisplayMode(ctypes.c_long DM)
    addfunc(lib, "SetDisplayMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["DM"] )
    #  bool GetFastMode(bool FM)
    addfunc(lib, "GetFastMode", restype = bool,
            argtypes = [bool],
            argnames = ["FM"] )
    #  ctypes.c_long SetFastMode(bool FM)
    addfunc(lib, "SetFastMode", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["FM"] )
    #  bool GetLinewidthMode(bool LM)
    addfunc(lib, "GetLinewidthMode", restype = bool,
            argtypes = [bool],
            argnames = ["LM"] )
    #  ctypes.c_long SetLinewidthMode(bool LM)
    addfunc(lib, "SetLinewidthMode", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["LM"] )
    #  bool GetDistanceMode(bool DM)
    addfunc(lib, "GetDistanceMode", restype = bool,
            argtypes = [bool],
            argnames = ["DM"] )
    #  ctypes.c_long SetDistanceMode(bool DM)
    addfunc(lib, "SetDistanceMode", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["DM"] )
    #  ctypes.c_long GetSwitcherMode(ctypes.c_long SM)
    addfunc(lib, "GetSwitcherMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["SM"] )
    #  ctypes.c_long SetSwitcherMode(ctypes.c_long SM)
    addfunc(lib, "SetSwitcherMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["SM"] )
    #  ctypes.c_long GetSwitcherChannel(ctypes.c_long CH)
    addfunc(lib, "GetSwitcherChannel", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["CH"] )
    #  ctypes.c_long SetSwitcherChannel(ctypes.c_long CH)
    addfunc(lib, "SetSwitcherChannel", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["CH"] )
    #  ctypes.c_long GetSwitcherSignalStates(ctypes.c_long Signal, lref Use, lref Show)
    addfunc(lib, "GetSwitcherSignalStates", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, lref, lref],
            argnames = ["Signal", "Use", "Show"] )
    #  ctypes.c_long SetSwitcherSignalStates(ctypes.c_long Signal, ctypes.c_long Use, ctypes.c_long Show)
    addfunc(lib, "SetSwitcherSignalStates", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["Signal", "Use", "Show"] )
    #  ctypes.c_long SetSwitcherSignal(ctypes.c_long Signal, ctypes.c_long Use, ctypes.c_long Show)
    addfunc(lib, "SetSwitcherSignal", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["Signal", "Use", "Show"] )
    #  ctypes.c_long GetAutoCalMode(ctypes.c_long ACM)
    addfunc(lib, "GetAutoCalMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["ACM"] )
    #  ctypes.c_long SetAutoCalMode(ctypes.c_long ACM)
    addfunc(lib, "SetAutoCalMode", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["ACM"] )
    #  ctypes.c_long GetAutoCalSetting(ctypes.c_long ACS, lref val, ctypes.c_long Res1, lref Res2)
    addfunc(lib, "GetAutoCalSetting", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, lref, ctypes.c_long, lref],
            argnames = ["ACS", "val", "Res1", "Res2"] )
    #  ctypes.c_long SetAutoCalSetting(ctypes.c_long ACS, ctypes.c_long val, ctypes.c_long Res1, ctypes.c_long Res2)
    addfunc(lib, "SetAutoCalSetting", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["ACS", "val", "Res1", "Res2"] )
    #  ctypes.c_long GetActiveChannel(ctypes.c_long Mode, lref Port, ctypes.c_long Res1)
    addfunc(lib, "GetActiveChannel", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, lref, ctypes.c_long],
            argnames = ["Mode", "Port", "Res1"] )
    #  ctypes.c_long SetActiveChannel(ctypes.c_long Mode, ctypes.c_long Port, ctypes.c_long CH, ctypes.c_long Res1)
    addfunc(lib, "SetActiveChannel", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["Mode", "Port", "CH", "Res1"] )
    #  ctypes.c_long GetChannelsCount(ctypes.c_long C)
    addfunc(lib, "GetChannelsCount", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["C"] )
    #  ctypes.c_ushort GetOperationState(ctypes.c_ushort OS)
    addfunc(lib, "GetOperationState", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["OS"] )
    #  ctypes.c_long Operation(ctypes.c_ushort Op)
    addfunc(lib, "Operation", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["Op"] )
    #  ctypes.c_long SetOperationFile(sref lpFile)
    addfunc(lib, "SetOperationFile", restype = ctypes.c_long,
            argtypes = [sref],
            argnames = ["lpFile"] )
    #  ctypes.c_long Calibration(ctypes.c_long Type, ctypes.c_long Unit, ctypes.c_double Value, ctypes.c_long Channel)
    addfunc(lib, "Calibration", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_long],
            argnames = ["Type", "Unit", "Value", "Channel"] )
    #  ctypes.c_long RaiseMeasurementEvent(ctypes.c_long Mode)
    addfunc(lib, "RaiseMeasurementEvent", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Mode"] )
    #  ctypes.c_long TriggerMeasurement(ctypes.c_long Action)
    addfunc(lib, "TriggerMeasurement", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Action"] )
    #  ctypes.c_long GetTriggerState(ctypes.c_long TS)
    addfunc(lib, "GetTriggerState", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["TS"] )
    #  ctypes.c_long GetInterval(ctypes.c_long I)
    addfunc(lib, "GetInterval", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["I"] )
    #  ctypes.c_long SetInterval(ctypes.c_long I)
    addfunc(lib, "SetInterval", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["I"] )
    #  bool GetIntervalMode(bool IM)
    addfunc(lib, "GetIntervalMode", restype = bool,
            argtypes = [bool],
            argnames = ["IM"] )
    #  ctypes.c_long SetIntervalMode(bool IM)
    addfunc(lib, "SetIntervalMode", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["IM"] )
    #  ctypes.c_long GetBackground(ctypes.c_long BG)
    addfunc(lib, "GetBackground", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["BG"] )
    #  ctypes.c_long SetBackground(ctypes.c_long BG)
    addfunc(lib, "SetBackground", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["BG"] )
    #  bool GetLinkState(bool LS)
    addfunc(lib, "GetLinkState", restype = bool,
            argtypes = [bool],
            argnames = ["LS"] )
    #  ctypes.c_long SetLinkState(bool LS)
    addfunc(lib, "SetLinkState", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["LS"] )
    #  None LinkSettingsDlg()
    addfunc(lib, "LinkSettingsDlg", restype = None,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_long GetPatternItemSize(ctypes.c_long Index)
    addfunc(lib, "GetPatternItemSize", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Index"] )
    #  ctypes.c_long GetPatternItemCount(ctypes.c_long Index)
    addfunc(lib, "GetPatternItemCount", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Index"] )
    #  ULONG_PTR GetPattern(ctypes.c_long Index)
    addfunc(lib, "GetPattern", restype = ULONG_PTR,
            argtypes = [ctypes.c_long],
            argnames = ["Index"] )
    #  ULONG_PTR GetPatternNum(ctypes.c_long Chn, ctypes.c_long Index)
    addfunc(lib, "GetPatternNum", restype = ULONG_PTR,
            argtypes = [ctypes.c_long, ctypes.c_long],
            argnames = ["Chn", "Index"] )
    #  ctypes.c_long GetPatternData(ctypes.c_long Index, ULONG_PTR PArray)
    addfunc(lib, "GetPatternData", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ULONG_PTR],
            argnames = ["Index", "PArray"] )
    #  ctypes.c_long GetPatternDataNum(ctypes.c_long Chn, ctypes.c_long Index, ULONG_PTR PArray)
    addfunc(lib, "GetPatternDataNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ULONG_PTR],
            argnames = ["Chn", "Index", "PArray"] )
    #  ctypes.c_long SetPattern(ctypes.c_long Index, ctypes.c_long iEnable)
    addfunc(lib, "SetPattern", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long],
            argnames = ["Index", "iEnable"] )
    #  ctypes.c_long SetPatternData(ctypes.c_long Index, ULONG_PTR PArray)
    addfunc(lib, "SetPatternData", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ULONG_PTR],
            argnames = ["Index", "PArray"] )
    #  bool GetAnalysisMode(bool AM)
    addfunc(lib, "GetAnalysisMode", restype = bool,
            argtypes = [bool],
            argnames = ["AM"] )
    #  ctypes.c_long SetAnalysisMode(bool AM)
    addfunc(lib, "SetAnalysisMode", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["AM"] )
    #  ctypes.c_long GetAnalysisItemSize(ctypes.c_long Index)
    addfunc(lib, "GetAnalysisItemSize", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Index"] )
    #  ctypes.c_long GetAnalysisItemCount(ctypes.c_long Index)
    addfunc(lib, "GetAnalysisItemCount", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Index"] )
    #  ULONG_PTR GetAnalysis(ctypes.c_long Index)
    addfunc(lib, "GetAnalysis", restype = ULONG_PTR,
            argtypes = [ctypes.c_long],
            argnames = ["Index"] )
    #  ctypes.c_long GetAnalysisData(ctypes.c_long Index, ULONG_PTR PArray)
    addfunc(lib, "GetAnalysisData", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ULONG_PTR],
            argnames = ["Index", "PArray"] )
    #  ctypes.c_long SetAnalysis(ctypes.c_long Index, ctypes.c_long iEnable)
    addfunc(lib, "SetAnalysis", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long],
            argnames = ["Index", "iEnable"] )
    #  ctypes.c_long GetMinPeak(ctypes.c_long M1)
    addfunc(lib, "GetMinPeak", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["M1"] )
    #  ctypes.c_long GetMinPeak2(ctypes.c_long M2)
    addfunc(lib, "GetMinPeak2", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["M2"] )
    #  ctypes.c_long GetMaxPeak(ctypes.c_long X1)
    addfunc(lib, "GetMaxPeak", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["X1"] )
    #  ctypes.c_long GetMaxPeak2(ctypes.c_long X2)
    addfunc(lib, "GetMaxPeak2", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["X2"] )
    #  ctypes.c_long GetAvgPeak(ctypes.c_long A1)
    addfunc(lib, "GetAvgPeak", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["A1"] )
    #  ctypes.c_long GetAvgPeak2(ctypes.c_long A2)
    addfunc(lib, "GetAvgPeak2", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["A2"] )
    #  ctypes.c_long SetAvgPeak(ctypes.c_long PA)
    addfunc(lib, "SetAvgPeak", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["PA"] )
    #  ctypes.c_long GetAmplitudeNum(ctypes.c_long num, ctypes.c_long Index, ctypes.c_long A)
    addfunc(lib, "GetAmplitudeNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["num", "Index", "A"] )
    #  ctypes.c_double GetIntensityNum(ctypes.c_long num, ctypes.c_double I)
    addfunc(lib, "GetIntensityNum", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["num", "I"] )
    #  ctypes.c_double GetPowerNum(ctypes.c_long num, ctypes.c_double P)
    addfunc(lib, "GetPowerNum", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["num", "P"] )
    #  ctypes.c_ushort GetDelay(ctypes.c_ushort D)
    addfunc(lib, "GetDelay", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["D"] )
    #  ctypes.c_long SetDelay(ctypes.c_ushort D)
    addfunc(lib, "SetDelay", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["D"] )
    #  ctypes.c_ushort GetShift(ctypes.c_ushort S)
    addfunc(lib, "GetShift", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["S"] )
    #  ctypes.c_long SetShift(ctypes.c_ushort S)
    addfunc(lib, "SetShift", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["S"] )
    #  ctypes.c_ushort GetShift2(ctypes.c_ushort S2)
    addfunc(lib, "GetShift2", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["S2"] )
    #  ctypes.c_long SetShift2(ctypes.c_ushort S2)
    addfunc(lib, "SetShift2", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["S2"] )
    #  bool GetDeviationMode(bool DM)
    addfunc(lib, "GetDeviationMode", restype = bool,
            argtypes = [bool],
            argnames = ["DM"] )
    #  ctypes.c_long SetDeviationMode(bool DM)
    addfunc(lib, "SetDeviationMode", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["DM"] )
    #  ctypes.c_double GetDeviationReference(ctypes.c_double DR)
    addfunc(lib, "GetDeviationReference", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["DR"] )
    #  ctypes.c_long SetDeviationReference(ctypes.c_double DR)
    addfunc(lib, "SetDeviationReference", restype = ctypes.c_long,
            argtypes = [ctypes.c_double],
            argnames = ["DR"] )
    #  ctypes.c_long GetDeviationSensitivity(ctypes.c_long DS)
    addfunc(lib, "GetDeviationSensitivity", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["DS"] )
    #  ctypes.c_long SetDeviationSensitivity(ctypes.c_long DS)
    addfunc(lib, "SetDeviationSensitivity", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["DS"] )
    #  ctypes.c_double GetDeviationSignal(ctypes.c_double DS)
    addfunc(lib, "GetDeviationSignal", restype = ctypes.c_double,
            argtypes = [ctypes.c_double],
            argnames = ["DS"] )
    #  ctypes.c_double GetDeviationSignalNum(ctypes.c_long Port, ctypes.c_double DS)
    addfunc(lib, "GetDeviationSignalNum", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["Port", "DS"] )
    #  ctypes.c_long SetDeviationSignal(ctypes.c_double DS)
    addfunc(lib, "SetDeviationSignal", restype = ctypes.c_long,
            argtypes = [ctypes.c_double],
            argnames = ["DS"] )
    #  ctypes.c_long SetDeviationSignalNum(ctypes.c_long Port, ctypes.c_double DS)
    addfunc(lib, "SetDeviationSignalNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["Port", "DS"] )
    #  ctypes.c_double RaiseDeviationSignal(ctypes.c_long iType, ctypes.c_double dSignal)
    addfunc(lib, "RaiseDeviationSignal", restype = ctypes.c_double,
            argtypes = [ctypes.c_long, ctypes.c_double],
            argnames = ["iType", "dSignal"] )
    #  ctypes.c_long GetPIDCourse(sref PIDC)
    addfunc(lib, "GetPIDCourse", restype = ctypes.c_long,
            argtypes = [sref],
            argnames = ["PIDC"] )
    #  ctypes.c_long SetPIDCourse(sref PIDC)
    addfunc(lib, "SetPIDCourse", restype = ctypes.c_long,
            argtypes = [sref],
            argnames = ["PIDC"] )
    #  ctypes.c_long GetPIDCourseNum(ctypes.c_long Port, sref PIDC)
    addfunc(lib, "GetPIDCourseNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, sref],
            argnames = ["Port", "PIDC"] )
    #  ctypes.c_long SetPIDCourseNum(ctypes.c_long Port, sref PIDC)
    addfunc(lib, "SetPIDCourseNum", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, sref],
            argnames = ["Port", "PIDC"] )
    #  ctypes.c_long GetPIDSetting(ctypes.c_long PS, ctypes.c_long Port, lref iSet, dref dSet)
    addfunc(lib, "GetPIDSetting", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, lref, dref],
            argnames = ["PS", "Port", "iSet", "dSet"] )
    #  ctypes.c_long SetPIDSetting(ctypes.c_long PS, ctypes.c_long Port, ctypes.c_long iSet, ctypes.c_double dSet)
    addfunc(lib, "SetPIDSetting", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double],
            argnames = ["PS", "Port", "iSet", "dSet"] )
    #  ctypes.c_long GetLaserControlSetting(ctypes.c_long PS, ctypes.c_long Port, lref iSet, dref dSet, sref sSet)
    addfunc(lib, "GetLaserControlSetting", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, lref, dref, sref],
            argnames = ["PS", "Port", "iSet", "dSet", "sSet"] )
    #  ctypes.c_long SetLaserControlSetting(ctypes.c_long PS, ctypes.c_long Port, ctypes.c_long iSet, ctypes.c_double dSet, sref sSet)
    addfunc(lib, "SetLaserControlSetting", restype = ctypes.c_long,
            argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double, sref],
            argnames = ["PS", "Port", "iSet", "dSet", "sSet"] )
    #  ctypes.c_long ClearPIDHistory(ctypes.c_long Port)
    addfunc(lib, "ClearPIDHistory", restype = ctypes.c_long,
            argtypes = [ctypes.c_long],
            argnames = ["Port"] )
    #  ctypes.c_double ConvertUnit(ctypes.c_double Val, ctypes.c_long uFrom, ctypes.c_long uTo)
    addfunc(lib, "ConvertUnit", restype = ctypes.c_double,
            argtypes = [ctypes.c_double, ctypes.c_long, ctypes.c_long],
            argnames = ["Val", "uFrom", "uTo"] )
    #  ctypes.c_double ConvertDeltaUnit(ctypes.c_double Base, ctypes.c_double Delta, ctypes.c_long uBase, ctypes.c_long uFrom, ctypes.c_long uTo)
    addfunc(lib, "ConvertDeltaUnit", restype = ctypes.c_double,
            argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long],
            argnames = ["Base", "Delta", "uBase", "uFrom", "uTo"] )
    #  bool GetReduced(bool R)
    addfunc(lib, "GetReduced", restype = bool,
            argtypes = [bool],
            argnames = ["R"] )
    #  ctypes.c_long SetReduced(bool R)
    addfunc(lib, "SetReduced", restype = ctypes.c_long,
            argtypes = [bool],
            argnames = ["R"] )
    #  ctypes.c_ushort GetScale(ctypes.c_ushort S)
    addfunc(lib, "GetScale", restype = ctypes.c_ushort,
            argtypes = [ctypes.c_ushort],
            argnames = ["S"] )
    #  ctypes.c_long SetScale(ctypes.c_ushort S)
    addfunc(lib, "SetScale", restype = ctypes.c_long,
            argtypes = [ctypes.c_ushort],
            argnames = ["S"] )


