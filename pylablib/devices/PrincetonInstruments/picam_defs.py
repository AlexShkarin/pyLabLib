##########   This file is generated automatically based on picam_advanced.h   ##########

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
piint=ctypes.c_int
piflt=ctypes.c_double
pibln=ctypes.c_int
pichar=ctypes.c_char
pi16s=ctypes.c_short
pi64s=ctypes.c_longlong
pi32f=ctypes.c_float
class PicamError(enum.IntEnum):
    PicamError_None                                 =_int32(0)
    PicamError_UnexpectedError                      =_int32(4)
    PicamError_UnexpectedNullPointer                =_int32(3)
    PicamError_InvalidPointer                       =_int32(35)
    PicamError_InvalidCount                         =_int32(39)
    PicamError_EnumerationValueNotDefined           =_int32(17)
    PicamError_InvalidOperation                     =_int32(42)
    PicamError_OperationCanceled                    =_int32(43)
    PicamError_LibraryNotInitialized                =_int32(1)
    PicamError_LibraryAlreadyInitialized            =_int32(5)
    PicamError_InvalidEnumeratedType                =_int32(16)
    PicamError_NotDiscoveringCameras                =_int32(18)
    PicamError_AlreadyDiscoveringCameras            =_int32(19)
    PicamError_NotDiscoveringAccessories            =_int32(48)
    PicamError_AlreadyDiscoveringAccessories        =_int32(49)
    PicamError_NoCamerasAvailable                   =_int32(34)
    PicamError_CameraAlreadyOpened                  =_int32(7)
    PicamError_InvalidCameraID                      =_int32(8)
    PicamError_NoAccessoriesAvailable               =_int32(45)
    PicamError_AccessoryAlreadyOpened               =_int32(46)
    PicamError_InvalidAccessoryID                   =_int32(47)
    PicamError_InvalidHandle                        =_int32(9)
    PicamError_DeviceCommunicationFailed            =_int32(15)
    PicamError_DeviceDisconnected                   =_int32(23)
    PicamError_DeviceOpenElsewhere                  =_int32(24)
    PicamError_InvalidDemoModel                     =_int32(6)
    PicamError_InvalidDemoSerialNumber              =_int32(21)
    PicamError_DemoAlreadyConnected                 =_int32(22)
    PicamError_DemoNotSupported                     =_int32(40)
    PicamError_ParameterHasInvalidValueType         =_int32(11)
    PicamError_ParameterHasInvalidConstraintType    =_int32(13)
    PicamError_ParameterDoesNotExist                =_int32(12)
    PicamError_ParameterValueIsReadOnly             =_int32(10)
    PicamError_InvalidParameterValue                =_int32(2)
    PicamError_InvalidConstraintCategory            =_int32(38)
    PicamError_ParameterValueIsIrrelevant           =_int32(14)
    PicamError_ParameterIsNotOnlineable             =_int32(25)
    PicamError_ParameterIsNotReadable               =_int32(26)
    PicamError_ParameterIsNotWaitableStatus         =_int32(50)
    PicamError_InvalidWaitableStatusParameterTimeOut=_int32(51)
    PicamError_InvalidParameterValues               =_int32(28)
    PicamError_ParametersNotCommitted               =_int32(29)
    PicamError_InvalidAcquisitionBuffer             =_int32(30)
    PicamError_InvalidReadoutCount                  =_int32(36)
    PicamError_InvalidReadoutTimeOut                =_int32(37)
    PicamError_InsufficientMemory                   =_int32(31)
    PicamError_AcquisitionInProgress                =_int32(20)
    PicamError_AcquisitionNotInProgress             =_int32(27)
    PicamError_TimeOutOccurred                      =_int32(32)
    PicamError_AcquisitionUpdatedHandlerRegistered  =_int32(33)
    PicamError_InvalidAcquisitionState              =_int32(44)
    PicamError_NondestructiveReadoutEnabled         =_int32(41)
    PicamError_ShutterOverheated                    =_int32(52)
    PicamError_CenterWavelengthFaulted              =_int32(54)
    PicamError_CameraFaulted                        =_int32(53)
dPicamError={a.name:a.value for a in PicamError}
drPicamError={a.value:a.name for a in PicamError}


class PicamEnumeratedType(enum.IntEnum):
    PicamEnumeratedType_Error                     =_int32(1)
    PicamEnumeratedType_EnumeratedType            =_int32(29)
    PicamEnumeratedType_Model                     =_int32(2)
    PicamEnumeratedType_ComputerInterface         =_int32(3)
    PicamEnumeratedType_DiscoveryAction           =_int32(26)
    PicamEnumeratedType_HandleType                =_int32(27)
    PicamEnumeratedType_ValueType                 =_int32(4)
    PicamEnumeratedType_ConstraintType            =_int32(5)
    PicamEnumeratedType_Parameter                 =_int32(6)
    PicamEnumeratedType_ActiveShutter             =_int32(53)
    PicamEnumeratedType_AdcAnalogGain             =_int32(7)
    PicamEnumeratedType_AdcQuality                =_int32(8)
    PicamEnumeratedType_CcdCharacteristicsMask    =_int32(9)
    PicamEnumeratedType_CenterWavelengthStatus    =_int32(51)
    PicamEnumeratedType_CoolingFanStatus          =_int32(56)
    PicamEnumeratedType_EMIccdGainControlMode     =_int32(42)
    PicamEnumeratedType_GateTrackingMask          =_int32(36)
    PicamEnumeratedType_GatingMode                =_int32(34)
    PicamEnumeratedType_GatingSpeed               =_int32(38)
    PicamEnumeratedType_GratingCoating            =_int32(48)
    PicamEnumeratedType_GratingType               =_int32(49)
    PicamEnumeratedType_IntensifierOptionsMask    =_int32(35)
    PicamEnumeratedType_IntensifierStatus         =_int32(33)
    PicamEnumeratedType_LaserOutputMode           =_int32(45)
    PicamEnumeratedType_LaserStatus               =_int32(54)
    PicamEnumeratedType_LightSource               =_int32(46)
    PicamEnumeratedType_LightSourceStatus         =_int32(47)
    PicamEnumeratedType_ModulationTrackingMask    =_int32(41)
    PicamEnumeratedType_OrientationMask           =_int32(10)
    PicamEnumeratedType_OutputSignal              =_int32(11)
    PicamEnumeratedType_PhosphorType              =_int32(39)
    PicamEnumeratedType_PhotocathodeSensitivity   =_int32(40)
    PicamEnumeratedType_PhotonDetectionMode       =_int32(43)
    PicamEnumeratedType_PixelFormat               =_int32(12)
    PicamEnumeratedType_ReadoutControlMode        =_int32(13)
    PicamEnumeratedType_SensorTemperatureStatus   =_int32(14)
    PicamEnumeratedType_SensorType                =_int32(15)
    PicamEnumeratedType_ShutterStatus             =_int32(52)
    PicamEnumeratedType_ShutterTimingMode         =_int32(16)
    PicamEnumeratedType_ShutterType               =_int32(50)
    PicamEnumeratedType_TimeStampsMask            =_int32(17)
    PicamEnumeratedType_TriggerCoupling           =_int32(30)
    PicamEnumeratedType_TriggerDetermination      =_int32(18)
    PicamEnumeratedType_TriggerResponse           =_int32(19)
    PicamEnumeratedType_TriggerSource             =_int32(31)
    PicamEnumeratedType_TriggerStatus             =_int32(55)
    PicamEnumeratedType_TriggerTermination        =_int32(32)
    PicamEnumeratedType_VacuumStatus              =_int32(57)
    PicamEnumeratedType_ValueAccess               =_int32(20)
    PicamEnumeratedType_DynamicsMask              =_int32(28)
    PicamEnumeratedType_ConstraintScope           =_int32(21)
    PicamEnumeratedType_ConstraintSeverity        =_int32(22)
    PicamEnumeratedType_ConstraintCategory        =_int32(23)
    PicamEnumeratedType_RoisConstraintRulesMask   =_int32(24)
    PicamEnumeratedType_AcquisitionErrorsMask     =_int32(25)
    PicamEnumeratedType_AcquisitionState          =_int32(37)
    PicamEnumeratedType_AcquisitionStateErrorsMask=_int32(44)
dPicamEnumeratedType={a.name:a.value for a in PicamEnumeratedType}
drPicamEnumeratedType={a.value:a.name for a in PicamEnumeratedType}


class PicamModel(enum.IntEnum):
    PicamModel_PIMteSeries              =_int32(1400)
    PicamModel_PIMte1024Series          =_int32(1401)
    PicamModel_PIMte1024F               =_int32(1402)
    PicamModel_PIMte1024B               =_int32(1403)
    PicamModel_PIMte1024BR              =_int32(1405)
    PicamModel_PIMte1024BUV             =_int32(1404)
    PicamModel_PIMte1024FTSeries        =_int32(1406)
    PicamModel_PIMte1024FT              =_int32(1407)
    PicamModel_PIMte1024BFT             =_int32(1408)
    PicamModel_PIMte1300Series          =_int32(1412)
    PicamModel_PIMte1300B               =_int32(1413)
    PicamModel_PIMte1300R               =_int32(1414)
    PicamModel_PIMte1300BR              =_int32(1415)
    PicamModel_PIMte2048Series          =_int32(1416)
    PicamModel_PIMte2048B               =_int32(1417)
    PicamModel_PIMte2048BR              =_int32(1418)
    PicamModel_PIMte2KSeries            =_int32(1409)
    PicamModel_PIMte2KB                 =_int32(1410)
    PicamModel_PIMte2KBUV               =_int32(1411)
    PicamModel_PIMte3Series             =_int32(2000)
    PicamModel_PIMte32048Series         =_int32(2001)
    PicamModel_PIMte32048B              =_int32(2002)
    PicamModel_PIMte34096Series         =_int32(2003)
    PicamModel_PIMte34096B              =_int32(2004)
    PicamModel_PIMte34096B_2            =_int32(2005)
    PicamModel_PixisSeries              =_int32(0)
    PicamModel_Pixis100Series           =_int32(1)
    PicamModel_Pixis100F                =_int32(2)
    PicamModel_Pixis100B                =_int32(6)
    PicamModel_Pixis100R                =_int32(3)
    PicamModel_Pixis100C                =_int32(4)
    PicamModel_Pixis100BR               =_int32(5)
    PicamModel_Pixis100BExcelon         =_int32(54)
    PicamModel_Pixis100BRExcelon        =_int32(55)
    PicamModel_PixisXO100B              =_int32(7)
    PicamModel_PixisXO100BR             =_int32(8)
    PicamModel_PixisXB100B              =_int32(68)
    PicamModel_PixisXB100BR             =_int32(69)
    PicamModel_Pixis256Series           =_int32(26)
    PicamModel_Pixis256F                =_int32(27)
    PicamModel_Pixis256B                =_int32(29)
    PicamModel_Pixis256E                =_int32(28)
    PicamModel_Pixis256BR               =_int32(30)
    PicamModel_PixisXB256BR             =_int32(31)
    PicamModel_Pixis400Series           =_int32(37)
    PicamModel_Pixis400F                =_int32(38)
    PicamModel_Pixis400B                =_int32(40)
    PicamModel_Pixis400R                =_int32(39)
    PicamModel_Pixis400BR               =_int32(41)
    PicamModel_Pixis400BExcelon         =_int32(56)
    PicamModel_Pixis400BRExcelon        =_int32(57)
    PicamModel_PixisXO400B              =_int32(42)
    PicamModel_PixisXB400BR             =_int32(70)
    PicamModel_Pixis512Series           =_int32(43)
    PicamModel_Pixis512F                =_int32(44)
    PicamModel_Pixis512B                =_int32(45)
    PicamModel_Pixis512BUV              =_int32(46)
    PicamModel_Pixis512BExcelon         =_int32(58)
    PicamModel_PixisXO512F              =_int32(49)
    PicamModel_PixisXO512B              =_int32(50)
    PicamModel_PixisXF512F              =_int32(48)
    PicamModel_PixisXF512B              =_int32(47)
    PicamModel_Pixis1024Series          =_int32(9)
    PicamModel_Pixis1024F               =_int32(10)
    PicamModel_Pixis1024B               =_int32(11)
    PicamModel_Pixis1024BR              =_int32(13)
    PicamModel_Pixis1024BUV             =_int32(12)
    PicamModel_Pixis1024BExcelon        =_int32(59)
    PicamModel_Pixis1024BRExcelon       =_int32(60)
    PicamModel_PixisXO1024F             =_int32(16)
    PicamModel_PixisXO1024B             =_int32(14)
    PicamModel_PixisXO1024BR            =_int32(15)
    PicamModel_PixisXF1024F             =_int32(17)
    PicamModel_PixisXF1024B             =_int32(18)
    PicamModel_PixisXB1024BR            =_int32(71)
    PicamModel_Pixis1300Series          =_int32(51)
    PicamModel_Pixis1300F               =_int32(52)
    PicamModel_Pixis1300F_2             =_int32(75)
    PicamModel_Pixis1300B               =_int32(53)
    PicamModel_Pixis1300BR              =_int32(73)
    PicamModel_Pixis1300BExcelon        =_int32(61)
    PicamModel_Pixis1300BRExcelon       =_int32(62)
    PicamModel_PixisXO1300B             =_int32(65)
    PicamModel_PixisXF1300B             =_int32(66)
    PicamModel_PixisXB1300R             =_int32(72)
    PicamModel_Pixis2048Series          =_int32(20)
    PicamModel_Pixis2048F               =_int32(21)
    PicamModel_Pixis2048B               =_int32(22)
    PicamModel_Pixis2048BR              =_int32(67)
    PicamModel_Pixis2048BExcelon        =_int32(63)
    PicamModel_Pixis2048BRExcelon       =_int32(74)
    PicamModel_PixisXO2048B             =_int32(23)
    PicamModel_PixisXF2048F             =_int32(25)
    PicamModel_PixisXF2048B             =_int32(24)
    PicamModel_Pixis2KSeries            =_int32(32)
    PicamModel_Pixis2KF                 =_int32(33)
    PicamModel_Pixis2KB                 =_int32(34)
    PicamModel_Pixis2KBUV               =_int32(36)
    PicamModel_Pixis2KBExcelon          =_int32(64)
    PicamModel_PixisXO2KB               =_int32(35)
    PicamModel_QuadroSeries             =_int32(100)
    PicamModel_Quadro4096               =_int32(101)
    PicamModel_Quadro4096_2             =_int32(103)
    PicamModel_Quadro4320               =_int32(102)
    PicamModel_ProEMSeries              =_int32(200)
    PicamModel_ProEM512Series           =_int32(203)
    PicamModel_ProEM512B                =_int32(201)
    PicamModel_ProEM512BK               =_int32(205)
    PicamModel_ProEM512BExcelon         =_int32(204)
    PicamModel_ProEM512BKExcelon        =_int32(206)
    PicamModel_ProEM1024Series          =_int32(207)
    PicamModel_ProEM1024B               =_int32(202)
    PicamModel_ProEM1024BExcelon        =_int32(208)
    PicamModel_ProEM1600Series          =_int32(209)
    PicamModel_ProEM1600xx2B            =_int32(212)
    PicamModel_ProEM1600xx2BExcelon     =_int32(210)
    PicamModel_ProEM1600xx4B            =_int32(213)
    PicamModel_ProEM1600xx4BExcelon     =_int32(211)
    PicamModel_ProEMPlusSeries          =_int32(600)
    PicamModel_ProEMPlus512Series       =_int32(603)
    PicamModel_ProEMPlus512B            =_int32(601)
    PicamModel_ProEMPlus512BK           =_int32(605)
    PicamModel_ProEMPlus512BExcelon     =_int32(604)
    PicamModel_ProEMPlus512BKExcelon    =_int32(606)
    PicamModel_ProEMPlus1024Series      =_int32(607)
    PicamModel_ProEMPlus1024B           =_int32(602)
    PicamModel_ProEMPlus1024BExcelon    =_int32(608)
    PicamModel_ProEMPlus1600Series      =_int32(609)
    PicamModel_ProEMPlus1600xx2B        =_int32(612)
    PicamModel_ProEMPlus1600xx2BExcelon =_int32(610)
    PicamModel_ProEMPlus1600xx4B        =_int32(613)
    PicamModel_ProEMPlus1600xx4BExcelon =_int32(611)
    PicamModel_ProEMHSSeries            =_int32(1200)
    PicamModel_ProEMHS512Series         =_int32(1201)
    PicamModel_ProEMHS512B              =_int32(1202)
    PicamModel_ProEMHS512BK             =_int32(1207)
    PicamModel_ProEMHS512BExcelon       =_int32(1203)
    PicamModel_ProEMHS512BKExcelon      =_int32(1208)
    PicamModel_ProEMHS512B_2            =_int32(1216)
    PicamModel_ProEMHS512BExcelon_2     =_int32(1217)
    PicamModel_ProEMHS1024Series        =_int32(1204)
    PicamModel_ProEMHS1024B             =_int32(1205)
    PicamModel_ProEMHS1024BExcelon      =_int32(1206)
    PicamModel_ProEMHS1024B_2           =_int32(1212)
    PicamModel_ProEMHS1024BExcelon_2    =_int32(1213)
    PicamModel_ProEMHS1024B_3           =_int32(1214)
    PicamModel_ProEMHS1024BExcelon_3    =_int32(1215)
    PicamModel_ProEMHS1K10Series        =_int32(1209)
    PicamModel_ProEMHS1KB10             =_int32(1210)
    PicamModel_ProEMHS1KB10Excelon      =_int32(1211)
    PicamModel_PIMax3Series             =_int32(300)
    PicamModel_PIMax31024I              =_int32(301)
    PicamModel_PIMax31024x256           =_int32(302)
    PicamModel_PIMax4Series             =_int32(700)
    PicamModel_PIMax41024ISeries        =_int32(703)
    PicamModel_PIMax41024I              =_int32(701)
    PicamModel_PIMax41024IRF            =_int32(704)
    PicamModel_PIMax41024FSeries        =_int32(710)
    PicamModel_PIMax41024F              =_int32(711)
    PicamModel_PIMax41024FRF            =_int32(712)
    PicamModel_PIMax41024x256Series     =_int32(705)
    PicamModel_PIMax41024x256           =_int32(702)
    PicamModel_PIMax41024x256RF         =_int32(706)
    PicamModel_PIMax42048Series         =_int32(716)
    PicamModel_PIMax42048F              =_int32(717)
    PicamModel_PIMax42048B              =_int32(718)
    PicamModel_PIMax42048FRF            =_int32(719)
    PicamModel_PIMax42048BRF            =_int32(720)
    PicamModel_PIMax4512EMSeries        =_int32(708)
    PicamModel_PIMax4512EM              =_int32(707)
    PicamModel_PIMax4512BEM             =_int32(709)
    PicamModel_PIMax41024EMSeries       =_int32(713)
    PicamModel_PIMax41024EM             =_int32(715)
    PicamModel_PIMax41024BEM            =_int32(714)
    PicamModel_PylonSeries              =_int32(400)
    PicamModel_Pylon100Series           =_int32(418)
    PicamModel_Pylon100F                =_int32(404)
    PicamModel_Pylon100B                =_int32(401)
    PicamModel_Pylon100BR               =_int32(407)
    PicamModel_Pylon100BExcelon         =_int32(425)
    PicamModel_Pylon100BRExcelon        =_int32(426)
    PicamModel_Pylon256Series           =_int32(419)
    PicamModel_Pylon256F                =_int32(409)
    PicamModel_Pylon256B                =_int32(410)
    PicamModel_Pylon256E                =_int32(411)
    PicamModel_Pylon256BR               =_int32(412)
    PicamModel_Pylon400Series           =_int32(420)
    PicamModel_Pylon400F                =_int32(405)
    PicamModel_Pylon400B                =_int32(402)
    PicamModel_Pylon400BR               =_int32(408)
    PicamModel_Pylon400BExcelon         =_int32(427)
    PicamModel_Pylon400BRExcelon        =_int32(428)
    PicamModel_Pylon1024Series          =_int32(421)
    PicamModel_Pylon1024B               =_int32(417)
    PicamModel_Pylon1024BExcelon        =_int32(429)
    PicamModel_Pylon1300Series          =_int32(422)
    PicamModel_Pylon1300F               =_int32(406)
    PicamModel_Pylon1300B               =_int32(403)
    PicamModel_Pylon1300R               =_int32(438)
    PicamModel_Pylon1300BR              =_int32(432)
    PicamModel_Pylon1300BExcelon        =_int32(430)
    PicamModel_Pylon1300BRExcelon       =_int32(433)
    PicamModel_Pylon2048Series          =_int32(423)
    PicamModel_Pylon2048F               =_int32(415)
    PicamModel_Pylon2048B               =_int32(434)
    PicamModel_Pylon2048BR              =_int32(416)
    PicamModel_Pylon2048BExcelon        =_int32(435)
    PicamModel_Pylon2048BRExcelon       =_int32(436)
    PicamModel_Pylon2KSeries            =_int32(424)
    PicamModel_Pylon2KF                 =_int32(413)
    PicamModel_Pylon2KB                 =_int32(414)
    PicamModel_Pylon2KBUV               =_int32(437)
    PicamModel_Pylon2KBExcelon          =_int32(431)
    PicamModel_PylonirSeries            =_int32(900)
    PicamModel_Pylonir1024Series        =_int32(901)
    PicamModel_Pylonir102422            =_int32(902)
    PicamModel_Pylonir102417            =_int32(903)
    PicamModel_PionirSeries             =_int32(500)
    PicamModel_Pionir640                =_int32(501)
    PicamModel_NirvanaSeries            =_int32(800)
    PicamModel_Nirvana640               =_int32(801)
    PicamModel_NirvanaSTSeries          =_int32(1300)
    PicamModel_NirvanaST640             =_int32(1301)
    PicamModel_NirvanaLNSeries          =_int32(1100)
    PicamModel_NirvanaLN640             =_int32(1101)
    PicamModel_NirvanaHSSeries          =_int32(2200)
    PicamModel_NirvanaHS                =_int32(2201)
    PicamModel_SophiaSeries             =_int32(1800)
    PicamModel_Sophia2048Series         =_int32(1801)
    PicamModel_Sophia2048B              =_int32(1802)
    PicamModel_Sophia2048BExcelon       =_int32(1803)
    PicamModel_SophiaXO2048B            =_int32(1804)
    PicamModel_SophiaXF2048B            =_int32(1805)
    PicamModel_SophiaXB2048B            =_int32(1806)
    PicamModel_Sophia2048135Series      =_int32(1807)
    PicamModel_Sophia2048135            =_int32(1808)
    PicamModel_Sophia2048B135           =_int32(1809)
    PicamModel_Sophia2048BR135          =_int32(1810)
    PicamModel_Sophia2048BUV135         =_int32(1844)
    PicamModel_Sophia2048B135Excelon    =_int32(1811)
    PicamModel_Sophia2048BR135Excelon   =_int32(1812)
    PicamModel_SophiaXO2048B135         =_int32(1813)
    PicamModel_SophiaXO2048BR135        =_int32(1814)
    PicamModel_Sophia2048B135Excelon_2  =_int32(1840)
    PicamModel_Sophia4096Series         =_int32(1826)
    PicamModel_Sophia4096B              =_int32(1827)
    PicamModel_SophiaXO4096B            =_int32(1829)
    PicamModel_SophiaXF4096B            =_int32(1830)
    PicamModel_SophiaXB4096B            =_int32(1831)
    PicamModel_Sophia4096B_2            =_int32(1841)
    PicamModel_Sophia4096HdrSeries      =_int32(1832)
    PicamModel_Sophia4096BHdr           =_int32(1833)
    PicamModel_Sophia4096BRHdr          =_int32(1834)
    PicamModel_SophiaXO4096BHdr         =_int32(1837)
    PicamModel_SophiaXO4096BRHdr        =_int32(1838)
    PicamModel_SophiaXF4096BHdr         =_int32(1839)
    PicamModel_SophiaXF4096BRHdr        =_int32(1828)
    PicamModel_SophiaXB4096BHdr         =_int32(1835)
    PicamModel_SophiaXB4096BRHdr        =_int32(1836)
    PicamModel_Sophia4096BHdr_2         =_int32(1842)
    PicamModel_Sophia4096BRHdr_2        =_int32(1843)
    PicamModel_BlazeSeries              =_int32(1500)
    PicamModel_Blaze100Series           =_int32(1507)
    PicamModel_Blaze100B                =_int32(1501)
    PicamModel_Blaze100BR               =_int32(1505)
    PicamModel_Blaze100HR               =_int32(1503)
    PicamModel_Blaze100BRLD             =_int32(1509)
    PicamModel_Blaze100BExcelon         =_int32(1511)
    PicamModel_Blaze100BRExcelon        =_int32(1513)
    PicamModel_Blaze100HRExcelon        =_int32(1515)
    PicamModel_Blaze100BRLDExcelon      =_int32(1517)
    PicamModel_Blaze400Series           =_int32(1508)
    PicamModel_Blaze400B                =_int32(1502)
    PicamModel_Blaze400BR               =_int32(1506)
    PicamModel_Blaze400HR               =_int32(1504)
    PicamModel_Blaze400BRLD             =_int32(1510)
    PicamModel_Blaze400BExcelon         =_int32(1512)
    PicamModel_Blaze400BRExcelon        =_int32(1514)
    PicamModel_Blaze400HRExcelon        =_int32(1516)
    PicamModel_Blaze400BRLDExcelon      =_int32(1518)
    PicamModel_FergieSeries             =_int32(1600)
    PicamModel_Fergie256Series          =_int32(1601)
    PicamModel_Fergie256B               =_int32(1602)
    PicamModel_Fergie256BR              =_int32(1607)
    PicamModel_Fergie256BExcelon        =_int32(1603)
    PicamModel_Fergie256BRExcelon       =_int32(1608)
    PicamModel_Fergie256FTSeries        =_int32(1604)
    PicamModel_Fergie256FFT             =_int32(1609)
    PicamModel_Fergie256BFT             =_int32(1605)
    PicamModel_Fergie256BRFT            =_int32(1610)
    PicamModel_Fergie256BFTExcelon      =_int32(1606)
    PicamModel_Fergie256BRFTExcelon     =_int32(1611)
    PicamModel_FergieIso81Series        =_int32(2100)
    PicamModel_FergieIso81256FTSeries   =_int32(2101)
    PicamModel_FergieIso81256BFTExcelon =_int32(2102)
    PicamModel_FergieIso81256BRFTExcelon=_int32(2103)
    PicamModel_FergieAccessorySeries    =_int32(1700)
    PicamModel_FergieLampSeries         =_int32(1701)
    PicamModel_FergieAEL                =_int32(1702)
    PicamModel_FergieQTH                =_int32(1703)
    PicamModel_FergieLaserSeries        =_int32(1704)
    PicamModel_FergieLaser785           =_int32(1705)
    PicamModel_FergieLaser532           =_int32(1706)
    PicamModel_KuroSeries               =_int32(1900)
    PicamModel_Kuro1200B                =_int32(1901)
    PicamModel_Kuro1608B                =_int32(1902)
    PicamModel_Kuro2048B                =_int32(1903)
    PicamModel_IntellicalAccessorySeries=_int32(2600)
    PicamModel_IntellicalLampSeries     =_int32(2601)
    PicamModel_IntellicalSwirQTH        =_int32(2602)
    PicamModel_TpirSeries               =_int32(2300)
    PicamModel_Tpir785Series            =_int32(2301)
    PicamModel_Tpir785100               =_int32(2302)
    PicamModel_Tpir785400               =_int32(2303)
    PicamModel_TpirHRSeries             =_int32(2400)
    PicamModel_Tpir785HRSeries          =_int32(2401)
    PicamModel_Tpir785HR100             =_int32(2402)
    PicamModel_Tpir785HR400             =_int32(2403)
dPicamModel={a.name:a.value for a in PicamModel}
drPicamModel={a.value:a.name for a in PicamModel}


class PicamComputerInterface(enum.IntEnum):
    PicamComputerInterface_Usb2           =_int32(1)
    PicamComputerInterface_1394A          =_int32(2)
    PicamComputerInterface_GigabitEthernet=_int32(3)
    PicamComputerInterface_Usb3           =_int32(4)
dPicamComputerInterface={a.name:a.value for a in PicamComputerInterface}
drPicamComputerInterface={a.value:a.name for a in PicamComputerInterface}


class PicamStringSize(enum.IntEnum):
    PicamStringSize_SensorName    =_int32(64)
    PicamStringSize_SerialNumber  =_int32(64)
    PicamStringSize_FirmwareName  =_int32(64)
    PicamStringSize_FirmwareDetail=_int32(256)
dPicamStringSize={a.name:a.value for a in PicamStringSize}
drPicamStringSize={a.value:a.name for a in PicamStringSize}


class PicamCameraID(ctypes.Structure):
    _fields_=[  ("model",ctypes.c_int),
                ("computer_interface",ctypes.c_int),
                ("sensor_name",pichar*PicamStringSize.PicamStringSize_SensorName.value),
                ("serial_number",pichar*PicamStringSize.PicamStringSize_SerialNumber.value) ]
PPicamCameraID=ctypes.POINTER(PicamCameraID)
class CPicamCameraID(ctypes_wrap.CStructWrapper):
    _struct=PicamCameraID


PicamHandle=ctypes.c_void_p
class PicamFirmwareDetail(ctypes.Structure):
    _fields_=[  ("name",pichar*PicamStringSize.PicamStringSize_FirmwareName.value),
                ("detail",pichar*PicamStringSize.PicamStringSize_FirmwareDetail.value) ]
PPicamFirmwareDetail=ctypes.POINTER(PicamFirmwareDetail)
class CPicamFirmwareDetail(ctypes_wrap.CStructWrapper):
    _struct=PicamFirmwareDetail


class PicamCalibrationPoint(ctypes.Structure):
    _fields_=[  ("x",piflt),
                ("y",piflt) ]
PPicamCalibrationPoint=ctypes.POINTER(PicamCalibrationPoint)
class CPicamCalibrationPoint(ctypes_wrap.CStructWrapper):
    _struct=PicamCalibrationPoint


class PicamCalibration(ctypes.Structure):
    _fields_=[  ("point_array",ctypes.POINTER(PicamCalibrationPoint)),
                ("point_count",piint) ]
PPicamCalibration=ctypes.POINTER(PicamCalibration)
class CPicamCalibration(ctypes_wrap.CStructWrapper):
    _struct=PicamCalibration


class PicamValueType(enum.IntEnum):
    PicamValueType_Integer      =_int32(1)
    PicamValueType_Boolean      =_int32(3)
    PicamValueType_Enumeration  =_int32(4)
    PicamValueType_LargeInteger =_int32(6)
    PicamValueType_FloatingPoint=_int32(2)
    PicamValueType_Rois         =_int32(5)
    PicamValueType_Pulse        =_int32(7)
    PicamValueType_Modulations  =_int32(8)
dPicamValueType={a.name:a.value for a in PicamValueType}
drPicamValueType={a.value:a.name for a in PicamValueType}


class PicamConstraintType(enum.IntEnum):
    PicamConstraintType_None       =_int32(1)
    PicamConstraintType_Range      =_int32(2)
    PicamConstraintType_Collection =_int32(3)
    PicamConstraintType_Rois       =_int32(4)
    PicamConstraintType_Pulse      =_int32(5)
    PicamConstraintType_Modulations=_int32(6)
dPicamConstraintType={a.name:a.value for a in PicamConstraintType}
drPicamConstraintType={a.value:a.name for a in PicamConstraintType}


class PicamParameter(enum.IntEnum):
    PicamParameter_ExposureTime                     =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+23))
    PicamParameter_ShutterTimingMode                =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+24))
    PicamParameter_ShutterOpeningDelay              =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+46))
    PicamParameter_ShutterClosingDelay              =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+25))
    PicamParameter_ShutterDelayResolution           =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+47))
    PicamParameter_InternalShutterType              =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+139))
    PicamParameter_InternalShutterStatus            =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+153))
    PicamParameter_ExternalShutterType              =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+152))
    PicamParameter_ExternalShutterStatus            =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+154))
    PicamParameter_ActiveShutter                    =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+155))
    PicamParameter_InactiveShutterTimingModeResult  =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+156))
    PicamParameter_GatingMode                       =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+93))
    PicamParameter_RepetitiveGate                   =_int32((((PicamConstraintType.PicamConstraintType_Pulse.value<<24)+(PicamValueType.PicamValueType_Pulse.value<<16))+94))
    PicamParameter_SequentialStartingGate           =_int32((((PicamConstraintType.PicamConstraintType_Pulse.value<<24)+(PicamValueType.PicamValueType_Pulse.value<<16))+95))
    PicamParameter_SequentialEndingGate             =_int32((((PicamConstraintType.PicamConstraintType_Pulse.value<<24)+(PicamValueType.PicamValueType_Pulse.value<<16))+96))
    PicamParameter_SequentialGateStepCount          =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_LargeInteger.value<<16))+97))
    PicamParameter_SequentialGateStepIterations     =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_LargeInteger.value<<16))+98))
    PicamParameter_DifStartingGate                  =_int32((((PicamConstraintType.PicamConstraintType_Pulse.value<<24)+(PicamValueType.PicamValueType_Pulse.value<<16))+102))
    PicamParameter_DifEndingGate                    =_int32((((PicamConstraintType.PicamConstraintType_Pulse.value<<24)+(PicamValueType.PicamValueType_Pulse.value<<16))+103))
    PicamParameter_EnableIntensifier                =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+86))
    PicamParameter_IntensifierStatus                =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+87))
    PicamParameter_IntensifierGain                  =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+88))
    PicamParameter_EMIccdGainControlMode            =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+123))
    PicamParameter_EMIccdGain                       =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+124))
    PicamParameter_PhosphorDecayDelay               =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+89))
    PicamParameter_PhosphorDecayDelayResolution     =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+90))
    PicamParameter_BracketGating                    =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+100))
    PicamParameter_IntensifierOptions               =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+101))
    PicamParameter_EnableModulation                 =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+111))
    PicamParameter_ModulationDuration               =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+118))
    PicamParameter_ModulationFrequency              =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+112))
    PicamParameter_RepetitiveModulationPhase        =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+113))
    PicamParameter_SequentialStartingModulationPhase=_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+114))
    PicamParameter_SequentialEndingModulationPhase  =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+115))
    PicamParameter_CustomModulationSequence         =_int32((((PicamConstraintType.PicamConstraintType_Modulations.value<<24)+(PicamValueType.PicamValueType_Modulations.value<<16))+119))
    PicamParameter_PhotocathodeSensitivity          =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+107))
    PicamParameter_GatingSpeed                      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+108))
    PicamParameter_PhosphorType                     =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+109))
    PicamParameter_IntensifierDiameter              =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+110))
    PicamParameter_AdcSpeed                         =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+33))
    PicamParameter_AdcBitDepth                      =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+34))
    PicamParameter_AdcAnalogGain                    =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+35))
    PicamParameter_AdcQuality                       =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+36))
    PicamParameter_AdcEMGain                        =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+53))
    PicamParameter_CorrectPixelBias                 =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+106))
    PicamParameter_TriggerSource                    =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+79))
    PicamParameter_TriggerResponse                  =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+30))
    PicamParameter_TriggerDetermination             =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+31))
    PicamParameter_TriggerFrequency                 =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+80))
    PicamParameter_TriggerTermination               =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+81))
    PicamParameter_TriggerCoupling                  =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+82))
    PicamParameter_TriggerThreshold                 =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+83))
    PicamParameter_TriggerDelay                     =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+164))
    PicamParameter_OutputSignal                     =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+32))
    PicamParameter_InvertOutputSignal               =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+52))
    PicamParameter_OutputSignal2                    =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+150))
    PicamParameter_InvertOutputSignal2              =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+151))
    PicamParameter_EnableAuxOutput                  =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+161))
    PicamParameter_AuxOutput                        =_int32((((PicamConstraintType.PicamConstraintType_Pulse.value<<24)+(PicamValueType.PicamValueType_Pulse.value<<16))+91))
    PicamParameter_EnableSyncMaster                 =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+84))
    PicamParameter_SyncMaster2Delay                 =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+85))
    PicamParameter_EnableModulationOutputSignal     =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+116))
    PicamParameter_ModulationOutputSignalFrequency  =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+117))
    PicamParameter_ModulationOutputSignalAmplitude  =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+120))
    PicamParameter_AnticipateTrigger                =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+131))
    PicamParameter_DelayFromPreTrigger              =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+132))
    PicamParameter_ReadoutControlMode               =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+26))
    PicamParameter_ReadoutTimeCalculation           =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+27))
    PicamParameter_ReadoutPortCount                 =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+28))
    PicamParameter_ReadoutOrientation               =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+54))
    PicamParameter_KineticsWindowHeight             =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+56))
    PicamParameter_SeNsRWindowHeight                =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+163))
    PicamParameter_VerticalShiftRate                =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+13))
    PicamParameter_Accumulations                    =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_LargeInteger.value<<16))+92))
    PicamParameter_EnableNondestructiveReadout      =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+128))
    PicamParameter_NondestructiveReadoutPeriod      =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+129))
    PicamParameter_Rois                             =_int32((((PicamConstraintType.PicamConstraintType_Rois.value<<24)+(PicamValueType.PicamValueType_Rois.value<<16))+37))
    PicamParameter_NormalizeOrientation             =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+39))
    PicamParameter_DisableDataFormatting            =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+55))
    PicamParameter_ReadoutCount                     =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_LargeInteger.value<<16))+40))
    PicamParameter_ExactReadoutCountMaximum         =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_LargeInteger.value<<16))+77))
    PicamParameter_PhotonDetectionMode              =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+125))
    PicamParameter_PhotonDetectionThreshold         =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+126))
    PicamParameter_PixelFormat                      =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+41))
    PicamParameter_FrameSize                        =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+42))
    PicamParameter_FrameStride                      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+43))
    PicamParameter_FramesPerReadout                 =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+44))
    PicamParameter_ReadoutStride                    =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+45))
    PicamParameter_PixelBitDepth                    =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+48))
    PicamParameter_ReadoutRateCalculation           =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+50))
    PicamParameter_OnlineReadoutRateCalculation     =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+99))
    PicamParameter_FrameRateCalculation             =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+51))
    PicamParameter_Orientation                      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+38))
    PicamParameter_TimeStamps                       =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+68))
    PicamParameter_TimeStampResolution              =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_LargeInteger.value<<16))+69))
    PicamParameter_TimeStampBitDepth                =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+70))
    PicamParameter_TrackFrames                      =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+71))
    PicamParameter_FrameTrackingBitDepth            =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+72))
    PicamParameter_GateTracking                     =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+104))
    PicamParameter_GateTrackingBitDepth             =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+105))
    PicamParameter_ModulationTracking               =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+121))
    PicamParameter_ModulationTrackingBitDepth       =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+122))
    PicamParameter_SensorType                       =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+57))
    PicamParameter_CcdCharacteristics               =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+58))
    PicamParameter_SensorActiveWidth                =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+59))
    PicamParameter_SensorActiveHeight               =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+60))
    PicamParameter_SensorActiveExtendedHeight       =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+159))
    PicamParameter_SensorActiveLeftMargin           =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+61))
    PicamParameter_SensorActiveTopMargin            =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+62))
    PicamParameter_SensorActiveRightMargin          =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+63))
    PicamParameter_SensorActiveBottomMargin         =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+64))
    PicamParameter_SensorMaskedHeight               =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+65))
    PicamParameter_SensorMaskedTopMargin            =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+66))
    PicamParameter_SensorMaskedBottomMargin         =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+67))
    PicamParameter_SensorSecondaryMaskedHeight      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+49))
    PicamParameter_SensorSecondaryActiveHeight      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+74))
    PicamParameter_PixelWidth                       =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+9))
    PicamParameter_PixelHeight                      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+10))
    PicamParameter_PixelGapWidth                    =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+11))
    PicamParameter_PixelGapHeight                   =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+12))
    PicamParameter_ApplicableStarDefectMapID        =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+166))
    PicamParameter_ActiveWidth                      =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+1))
    PicamParameter_ActiveHeight                     =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+2))
    PicamParameter_ActiveExtendedHeight             =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+160))
    PicamParameter_ActiveLeftMargin                 =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+3))
    PicamParameter_ActiveTopMargin                  =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+4))
    PicamParameter_ActiveRightMargin                =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+5))
    PicamParameter_ActiveBottomMargin               =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+6))
    PicamParameter_MaskedHeight                     =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+7))
    PicamParameter_MaskedTopMargin                  =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+8))
    PicamParameter_MaskedBottomMargin               =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+73))
    PicamParameter_SecondaryMaskedHeight            =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+75))
    PicamParameter_SecondaryActiveHeight            =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+76))
    PicamParameter_CleanSectionFinalHeight          =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+17))
    PicamParameter_CleanSectionFinalHeightCount     =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+18))
    PicamParameter_CleanSerialRegister              =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+19))
    PicamParameter_CleanCycleCount                  =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+20))
    PicamParameter_CleanCycleHeight                 =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_Integer.value<<16))+21))
    PicamParameter_CleanBeforeExposure              =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+78))
    PicamParameter_CleanUntilTrigger                =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+22))
    PicamParameter_StopCleaningOnPreTrigger         =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+130))
    PicamParameter_SensorTemperatureSetPoint        =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+14))
    PicamParameter_SensorTemperatureReading         =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+15))
    PicamParameter_SensorTemperatureStatus          =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+16))
    PicamParameter_DisableCoolingFan                =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+29))
    PicamParameter_CoolingFanStatus                 =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+162))
    PicamParameter_EnableSensorWindowHeater         =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Boolean.value<<16))+127))
    PicamParameter_VacuumStatus                     =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+165))
    PicamParameter_CenterWavelengthSetPoint         =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+140))
    PicamParameter_CenterWavelengthReading          =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+141))
    PicamParameter_CenterWavelengthStatus           =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+149))
    PicamParameter_GratingType                      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+142))
    PicamParameter_GratingCoating                   =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+143))
    PicamParameter_GratingGrooveDensity             =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+144))
    PicamParameter_GratingBlazingWavelength         =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+145))
    PicamParameter_FocalLength                      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+146))
    PicamParameter_InclusionAngle                   =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+147))
    PicamParameter_SensorAngle                      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+148))
    PicamParameter_LaserOutputMode                  =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+137))
    PicamParameter_LaserPower                       =_int32((((PicamConstraintType.PicamConstraintType_Range.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+138))
    PicamParameter_LaserWavelength                  =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+167))
    PicamParameter_LaserStatus                      =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+157))
    PicamParameter_InputTriggerStatus               =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+158))
    PicamParameter_LightSource                      =_int32((((PicamConstraintType.PicamConstraintType_Collection.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+133))
    PicamParameter_LightSourceStatus                =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_Enumeration.value<<16))+134))
    PicamParameter_Age                              =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+135))
    PicamParameter_LifeExpectancy                   =_int32((((PicamConstraintType.PicamConstraintType_None.value<<24)+(PicamValueType.PicamValueType_FloatingPoint.value<<16))+136))
dPicamParameter={a.name:a.value for a in PicamParameter}
drPicamParameter={a.value:a.name for a in PicamParameter}


class PicamRoi(ctypes.Structure):
    _fields_=[  ("x",piint),
                ("width",piint),
                ("x_binning",piint),
                ("y",piint),
                ("height",piint),
                ("y_binning",piint) ]
PPicamRoi=ctypes.POINTER(PicamRoi)
class CPicamRoi(ctypes_wrap.CStructWrapper):
    _struct=PicamRoi


class PicamRois(ctypes.Structure):
    _fields_=[  ("roi_array",ctypes.POINTER(PicamRoi)),
                ("roi_count",piint) ]
PPicamRois=ctypes.POINTER(PicamRois)
class CPicamRois(ctypes_wrap.CStructWrapper):
    _struct=PicamRois


class PicamPulse(ctypes.Structure):
    _fields_=[  ("delay",piflt),
                ("width",piflt) ]
PPicamPulse=ctypes.POINTER(PicamPulse)
class CPicamPulse(ctypes_wrap.CStructWrapper):
    _struct=PicamPulse


class PicamModulation(ctypes.Structure):
    _fields_=[  ("duration",piflt),
                ("frequency",piflt),
                ("phase",piflt),
                ("output_signal_frequency",piflt) ]
PPicamModulation=ctypes.POINTER(PicamModulation)
class CPicamModulation(ctypes_wrap.CStructWrapper):
    _struct=PicamModulation


class PicamModulations(ctypes.Structure):
    _fields_=[  ("modulation_array",ctypes.POINTER(PicamModulation)),
                ("modulation_count",piint) ]
PPicamModulations=ctypes.POINTER(PicamModulations)
class CPicamModulations(ctypes_wrap.CStructWrapper):
    _struct=PicamModulations


class PicamActiveShutter(enum.IntEnum):
    PicamActiveShutter_None    =_int32(1)
    PicamActiveShutter_Internal=_int32(2)
    PicamActiveShutter_External=_int32(3)
dPicamActiveShutter={a.name:a.value for a in PicamActiveShutter}
drPicamActiveShutter={a.value:a.name for a in PicamActiveShutter}


class PicamAdcAnalogGain(enum.IntEnum):
    PicamAdcAnalogGain_Low   =_int32(1)
    PicamAdcAnalogGain_Medium=_int32(2)
    PicamAdcAnalogGain_High  =_int32(3)
dPicamAdcAnalogGain={a.name:a.value for a in PicamAdcAnalogGain}
drPicamAdcAnalogGain={a.value:a.name for a in PicamAdcAnalogGain}


class PicamAdcQuality(enum.IntEnum):
    PicamAdcQuality_LowNoise          =_int32(1)
    PicamAdcQuality_HighCapacity      =_int32(2)
    PicamAdcQuality_HighSpeed         =_int32(4)
    PicamAdcQuality_ElectronMultiplied=_int32(3)
dPicamAdcQuality={a.name:a.value for a in PicamAdcQuality}
drPicamAdcQuality={a.value:a.name for a in PicamAdcQuality}


class PicamCcdCharacteristicsMask(enum.IntEnum):
    PicamCcdCharacteristicsMask_None                =_int32(0x000)
    PicamCcdCharacteristicsMask_BackIlluminated     =_int32(0x001)
    PicamCcdCharacteristicsMask_DeepDepleted        =_int32(0x002)
    PicamCcdCharacteristicsMask_OpenElectrode       =_int32(0x004)
    PicamCcdCharacteristicsMask_UVEnhanced          =_int32(0x008)
    PicamCcdCharacteristicsMask_ExcelonEnabled      =_int32(0x010)
    PicamCcdCharacteristicsMask_SecondaryMask       =_int32(0x020)
    PicamCcdCharacteristicsMask_Multiport           =_int32(0x040)
    PicamCcdCharacteristicsMask_AdvancedInvertedMode=_int32(0x080)
    PicamCcdCharacteristicsMask_HighResistivity     =_int32(0x100)
dPicamCcdCharacteristicsMask={a.name:a.value for a in PicamCcdCharacteristicsMask}
drPicamCcdCharacteristicsMask={a.value:a.name for a in PicamCcdCharacteristicsMask}


class PicamCenterWavelengthStatus(enum.IntEnum):
    PicamCenterWavelengthStatus_Moving    =_int32(1)
    PicamCenterWavelengthStatus_Stationary=_int32(2)
    PicamCenterWavelengthStatus_Faulted   =_int32(3)
dPicamCenterWavelengthStatus={a.name:a.value for a in PicamCenterWavelengthStatus}
drPicamCenterWavelengthStatus={a.value:a.name for a in PicamCenterWavelengthStatus}


class PicamCoolingFanStatus(enum.IntEnum):
    PicamCoolingFanStatus_Off     =_int32(1)
    PicamCoolingFanStatus_On      =_int32(2)
    PicamCoolingFanStatus_ForcedOn=_int32(3)
dPicamCoolingFanStatus={a.name:a.value for a in PicamCoolingFanStatus}
drPicamCoolingFanStatus={a.value:a.name for a in PicamCoolingFanStatus}


class PicamEMIccdGainControlMode(enum.IntEnum):
    PicamEMIccdGainControlMode_Optimal=_int32(1)
    PicamEMIccdGainControlMode_Manual =_int32(2)
dPicamEMIccdGainControlMode={a.name:a.value for a in PicamEMIccdGainControlMode}
drPicamEMIccdGainControlMode={a.value:a.name for a in PicamEMIccdGainControlMode}


class PicamGateTrackingMask(enum.IntEnum):
    PicamGateTrackingMask_None =_int32(0x0)
    PicamGateTrackingMask_Delay=_int32(0x1)
    PicamGateTrackingMask_Width=_int32(0x2)
dPicamGateTrackingMask={a.name:a.value for a in PicamGateTrackingMask}
drPicamGateTrackingMask={a.value:a.name for a in PicamGateTrackingMask}


class PicamGatingMode(enum.IntEnum):
    PicamGatingMode_Disabled  =_int32(4)
    PicamGatingMode_Repetitive=_int32(1)
    PicamGatingMode_Sequential=_int32(2)
    PicamGatingMode_Custom    =_int32(3)
dPicamGatingMode={a.name:a.value for a in PicamGatingMode}
drPicamGatingMode={a.value:a.name for a in PicamGatingMode}


class PicamGatingSpeed(enum.IntEnum):
    PicamGatingSpeed_Fast=_int32(1)
    PicamGatingSpeed_Slow=_int32(2)
dPicamGatingSpeed={a.name:a.value for a in PicamGatingSpeed}
drPicamGatingSpeed={a.value:a.name for a in PicamGatingSpeed}


class PicamGratingCoating(enum.IntEnum):
    PicamGratingCoating_Al    =_int32(1)
    PicamGratingCoating_AlMgF2=_int32(4)
    PicamGratingCoating_Ag    =_int32(2)
    PicamGratingCoating_Au    =_int32(3)
dPicamGratingCoating={a.name:a.value for a in PicamGratingCoating}
drPicamGratingCoating={a.value:a.name for a in PicamGratingCoating}


class PicamGratingType(enum.IntEnum):
    PicamGratingType_Ruled             =_int32(1)
    PicamGratingType_HolographicVisible=_int32(2)
    PicamGratingType_HolographicNir    =_int32(3)
    PicamGratingType_HolographicUV     =_int32(4)
    PicamGratingType_Mirror            =_int32(5)
dPicamGratingType={a.name:a.value for a in PicamGratingType}
drPicamGratingType={a.value:a.name for a in PicamGratingType}


class PicamIntensifierOptionsMask(enum.IntEnum):
    PicamIntensifierOptionsMask_None               =_int32(0x0)
    PicamIntensifierOptionsMask_McpGating          =_int32(0x1)
    PicamIntensifierOptionsMask_SubNanosecondGating=_int32(0x2)
    PicamIntensifierOptionsMask_Modulation         =_int32(0x4)
dPicamIntensifierOptionsMask={a.name:a.value for a in PicamIntensifierOptionsMask}
drPicamIntensifierOptionsMask={a.value:a.name for a in PicamIntensifierOptionsMask}


class PicamIntensifierStatus(enum.IntEnum):
    PicamIntensifierStatus_PoweredOff=_int32(1)
    PicamIntensifierStatus_PoweredOn =_int32(2)
dPicamIntensifierStatus={a.name:a.value for a in PicamIntensifierStatus}
drPicamIntensifierStatus={a.value:a.name for a in PicamIntensifierStatus}


class PicamLaserOutputMode(enum.IntEnum):
    PicamLaserOutputMode_Disabled      =_int32(1)
    PicamLaserOutputMode_ContinuousWave=_int32(2)
    PicamLaserOutputMode_Pulsed        =_int32(3)
dPicamLaserOutputMode={a.name:a.value for a in PicamLaserOutputMode}
drPicamLaserOutputMode={a.value:a.name for a in PicamLaserOutputMode}


class PicamLaserStatus(enum.IntEnum):
    PicamLaserStatus_Disarmed=_int32(1)
    PicamLaserStatus_Unarmed =_int32(2)
    PicamLaserStatus_Arming  =_int32(3)
    PicamLaserStatus_Armed   =_int32(4)
dPicamLaserStatus={a.name:a.value for a in PicamLaserStatus}
drPicamLaserStatus={a.value:a.name for a in PicamLaserStatus}


class PicamLightSource(enum.IntEnum):
    PicamLightSource_Disabled=_int32(1)
    PicamLightSource_Hg      =_int32(2)
    PicamLightSource_NeAr    =_int32(3)
    PicamLightSource_Qth     =_int32(4)
dPicamLightSource={a.name:a.value for a in PicamLightSource}
drPicamLightSource={a.value:a.name for a in PicamLightSource}


class PicamLightSourceStatus(enum.IntEnum):
    PicamLightSourceStatus_Unstable=_int32(1)
    PicamLightSourceStatus_Stable  =_int32(2)
dPicamLightSourceStatus={a.name:a.value for a in PicamLightSourceStatus}
drPicamLightSourceStatus={a.value:a.name for a in PicamLightSourceStatus}


class PicamModulationTrackingMask(enum.IntEnum):
    PicamModulationTrackingMask_None                 =_int32(0x0)
    PicamModulationTrackingMask_Duration             =_int32(0x1)
    PicamModulationTrackingMask_Frequency            =_int32(0x2)
    PicamModulationTrackingMask_Phase                =_int32(0x4)
    PicamModulationTrackingMask_OutputSignalFrequency=_int32(0x8)
dPicamModulationTrackingMask={a.name:a.value for a in PicamModulationTrackingMask}
drPicamModulationTrackingMask={a.value:a.name for a in PicamModulationTrackingMask}


class PicamOrientationMask(enum.IntEnum):
    PicamOrientationMask_Normal             =_int32(0x0)
    PicamOrientationMask_FlippedHorizontally=_int32(0x1)
    PicamOrientationMask_FlippedVertically  =_int32(0x2)
dPicamOrientationMask={a.name:a.value for a in PicamOrientationMask}
drPicamOrientationMask={a.value:a.name for a in PicamOrientationMask}


class PicamOutputSignal(enum.IntEnum):
    PicamOutputSignal_Acquiring                     =_int32(6)
    PicamOutputSignal_AlwaysHigh                    =_int32(5)
    PicamOutputSignal_AlwaysLow                     =_int32(4)
    PicamOutputSignal_AuxOutput                     =_int32(14)
    PicamOutputSignal_Busy                          =_int32(3)
    PicamOutputSignal_EffectivelyExposing           =_int32(9)
    PicamOutputSignal_EffectivelyExposingAlternation=_int32(15)
    PicamOutputSignal_Exposing                      =_int32(8)
    PicamOutputSignal_Gate                          =_int32(13)
    PicamOutputSignal_InternalTriggerT0             =_int32(12)
    PicamOutputSignal_NotReadingOut                 =_int32(1)
    PicamOutputSignal_ReadingOut                    =_int32(10)
    PicamOutputSignal_ShiftingUnderMask             =_int32(7)
    PicamOutputSignal_ShutterOpen                   =_int32(2)
    PicamOutputSignal_WaitingForTrigger             =_int32(11)
dPicamOutputSignal={a.name:a.value for a in PicamOutputSignal}
drPicamOutputSignal={a.value:a.name for a in PicamOutputSignal}


class PicamPhosphorType(enum.IntEnum):
    PicamPhosphorType_P43=_int32(1)
    PicamPhosphorType_P46=_int32(2)
dPicamPhosphorType={a.name:a.value for a in PicamPhosphorType}
drPicamPhosphorType={a.value:a.name for a in PicamPhosphorType}


class PicamPhotocathodeSensitivity(enum.IntEnum):
    PicamPhotocathodeSensitivity_RedBlue         =_int32(1)
    PicamPhotocathodeSensitivity_SuperRed        =_int32(7)
    PicamPhotocathodeSensitivity_SuperBlue       =_int32(2)
    PicamPhotocathodeSensitivity_UV              =_int32(3)
    PicamPhotocathodeSensitivity_SolarBlind      =_int32(10)
    PicamPhotocathodeSensitivity_Unigen2Filmless =_int32(4)
    PicamPhotocathodeSensitivity_InGaAsFilmless  =_int32(9)
    PicamPhotocathodeSensitivity_HighQEFilmless  =_int32(5)
    PicamPhotocathodeSensitivity_HighRedFilmless =_int32(8)
    PicamPhotocathodeSensitivity_HighBlueFilmless=_int32(6)
dPicamPhotocathodeSensitivity={a.name:a.value for a in PicamPhotocathodeSensitivity}
drPicamPhotocathodeSensitivity={a.value:a.name for a in PicamPhotocathodeSensitivity}


class PicamPhotonDetectionMode(enum.IntEnum):
    PicamPhotonDetectionMode_Disabled    =_int32(1)
    PicamPhotonDetectionMode_Thresholding=_int32(2)
    PicamPhotonDetectionMode_Clipping    =_int32(3)
dPicamPhotonDetectionMode={a.name:a.value for a in PicamPhotonDetectionMode}
drPicamPhotonDetectionMode={a.value:a.name for a in PicamPhotonDetectionMode}


class PicamPixelFormat(enum.IntEnum):
    PicamPixelFormat_Monochrome16Bit=_int32(1)
    PicamPixelFormat_Monochrome32Bit=_int32(2)
dPicamPixelFormat={a.name:a.value for a in PicamPixelFormat}
drPicamPixelFormat={a.value:a.name for a in PicamPixelFormat}


class PicamReadoutControlMode(enum.IntEnum):
    PicamReadoutControlMode_FullFrame          =_int32(1)
    PicamReadoutControlMode_FrameTransfer      =_int32(2)
    PicamReadoutControlMode_Interline          =_int32(5)
    PicamReadoutControlMode_RollingShutter     =_int32(8)
    PicamReadoutControlMode_ExposeDuringReadout=_int32(9)
    PicamReadoutControlMode_Kinetics           =_int32(3)
    PicamReadoutControlMode_SpectraKinetics    =_int32(4)
    PicamReadoutControlMode_Dif                =_int32(6)
    PicamReadoutControlMode_SeNsR              =_int32(7)
dPicamReadoutControlMode={a.name:a.value for a in PicamReadoutControlMode}
drPicamReadoutControlMode={a.value:a.name for a in PicamReadoutControlMode}


class PicamSensorTemperatureStatus(enum.IntEnum):
    PicamSensorTemperatureStatus_Unlocked=_int32(1)
    PicamSensorTemperatureStatus_Locked  =_int32(2)
    PicamSensorTemperatureStatus_Faulted =_int32(3)
dPicamSensorTemperatureStatus={a.name:a.value for a in PicamSensorTemperatureStatus}
drPicamSensorTemperatureStatus={a.value:a.name for a in PicamSensorTemperatureStatus}


class PicamSensorType(enum.IntEnum):
    PicamSensorType_Ccd   =_int32(1)
    PicamSensorType_InGaAs=_int32(2)
    PicamSensorType_Cmos  =_int32(3)
dPicamSensorType={a.name:a.value for a in PicamSensorType}
drPicamSensorType={a.value:a.name for a in PicamSensorType}


class PicamShutterStatus(enum.IntEnum):
    PicamShutterStatus_NotConnected=_int32(1)
    PicamShutterStatus_Connected   =_int32(2)
    PicamShutterStatus_Overheated  =_int32(3)
dPicamShutterStatus={a.name:a.value for a in PicamShutterStatus}
drPicamShutterStatus={a.value:a.name for a in PicamShutterStatus}


class PicamShutterTimingMode(enum.IntEnum):
    PicamShutterTimingMode_Normal           =_int32(1)
    PicamShutterTimingMode_AlwaysClosed     =_int32(2)
    PicamShutterTimingMode_AlwaysOpen       =_int32(3)
    PicamShutterTimingMode_OpenBeforeTrigger=_int32(4)
dPicamShutterTimingMode={a.name:a.value for a in PicamShutterTimingMode}
drPicamShutterTimingMode={a.value:a.name for a in PicamShutterTimingMode}


class PicamShutterType(enum.IntEnum):
    PicamShutterType_None              =_int32(1)
    PicamShutterType_VincentCS25       =_int32(2)
    PicamShutterType_VincentCS45       =_int32(3)
    PicamShutterType_VincentCS90       =_int32(9)
    PicamShutterType_VincentDSS10      =_int32(8)
    PicamShutterType_VincentVS25       =_int32(4)
    PicamShutterType_VincentVS35       =_int32(5)
    PicamShutterType_ProntorMagnetic0  =_int32(6)
    PicamShutterType_ProntorMagneticE40=_int32(7)
dPicamShutterType={a.name:a.value for a in PicamShutterType}
drPicamShutterType={a.value:a.name for a in PicamShutterType}


class PicamTimeStampsMask(enum.IntEnum):
    PicamTimeStampsMask_None           =_int32(0x0)
    PicamTimeStampsMask_ExposureStarted=_int32(0x1)
    PicamTimeStampsMask_ExposureEnded  =_int32(0x2)
dPicamTimeStampsMask={a.name:a.value for a in PicamTimeStampsMask}
drPicamTimeStampsMask={a.value:a.name for a in PicamTimeStampsMask}


class PicamTriggerCoupling(enum.IntEnum):
    PicamTriggerCoupling_AC=_int32(1)
    PicamTriggerCoupling_DC=_int32(2)
dPicamTriggerCoupling={a.name:a.value for a in PicamTriggerCoupling}
drPicamTriggerCoupling={a.value:a.name for a in PicamTriggerCoupling}


class PicamTriggerDetermination(enum.IntEnum):
    PicamTriggerDetermination_PositivePolarity      =_int32(1)
    PicamTriggerDetermination_NegativePolarity      =_int32(2)
    PicamTriggerDetermination_RisingEdge            =_int32(3)
    PicamTriggerDetermination_FallingEdge           =_int32(4)
    PicamTriggerDetermination_AlternatingEdgeRising =_int32(5)
    PicamTriggerDetermination_AlternatingEdgeFalling=_int32(6)
dPicamTriggerDetermination={a.name:a.value for a in PicamTriggerDetermination}
drPicamTriggerDetermination={a.value:a.name for a in PicamTriggerDetermination}


class PicamTriggerResponse(enum.IntEnum):
    PicamTriggerResponse_NoResponse              =_int32(1)
    PicamTriggerResponse_StartOnSingleTrigger    =_int32(5)
    PicamTriggerResponse_ReadoutPerTrigger       =_int32(2)
    PicamTriggerResponse_ShiftPerTrigger         =_int32(3)
    PicamTriggerResponse_GatePerTrigger          =_int32(6)
    PicamTriggerResponse_ExposeDuringTriggerPulse=_int32(4)
dPicamTriggerResponse={a.name:a.value for a in PicamTriggerResponse}
drPicamTriggerResponse={a.value:a.name for a in PicamTriggerResponse}


class PicamTriggerSource(enum.IntEnum):
    PicamTriggerSource_None    =_int32(3)
    PicamTriggerSource_Internal=_int32(2)
    PicamTriggerSource_External=_int32(1)
dPicamTriggerSource={a.name:a.value for a in PicamTriggerSource}
drPicamTriggerSource={a.value:a.name for a in PicamTriggerSource}


class PicamTriggerStatus(enum.IntEnum):
    PicamTriggerStatus_NotConnected=_int32(1)
    PicamTriggerStatus_Connected   =_int32(2)
dPicamTriggerStatus={a.name:a.value for a in PicamTriggerStatus}
drPicamTriggerStatus={a.value:a.name for a in PicamTriggerStatus}


class PicamTriggerTermination(enum.IntEnum):
    PicamTriggerTermination_FiftyOhms    =_int32(1)
    PicamTriggerTermination_HighImpedance=_int32(2)
dPicamTriggerTermination={a.name:a.value for a in PicamTriggerTermination}
drPicamTriggerTermination={a.value:a.name for a in PicamTriggerTermination}


class PicamVacuumStatus(enum.IntEnum):
    PicamVacuumStatus_Sufficient=_int32(1)
    PicamVacuumStatus_Low       =_int32(2)
dPicamVacuumStatus={a.name:a.value for a in PicamVacuumStatus}
drPicamVacuumStatus={a.value:a.name for a in PicamVacuumStatus}


class PicamStatusPurview(ctypes.Structure):
    _fields_=[  ("values_array",ctypes.POINTER(piint)),
                ("values_count",piint) ]
PPicamStatusPurview=ctypes.POINTER(PicamStatusPurview)
class CPicamStatusPurview(ctypes_wrap.CStructWrapper):
    _struct=PicamStatusPurview


class PicamValueAccess(enum.IntEnum):
    PicamValueAccess_ReadOnly        =_int32(1)
    PicamValueAccess_ReadWriteTrivial=_int32(3)
    PicamValueAccess_ReadWrite       =_int32(2)
dPicamValueAccess={a.name:a.value for a in PicamValueAccess}
drPicamValueAccess={a.value:a.name for a in PicamValueAccess}


class PicamConstraintScope(enum.IntEnum):
    PicamConstraintScope_Independent=_int32(1)
    PicamConstraintScope_Dependent  =_int32(2)
dPicamConstraintScope={a.name:a.value for a in PicamConstraintScope}
drPicamConstraintScope={a.value:a.name for a in PicamConstraintScope}


class PicamConstraintSeverity(enum.IntEnum):
    PicamConstraintSeverity_Error  =_int32(1)
    PicamConstraintSeverity_Warning=_int32(2)
dPicamConstraintSeverity={a.name:a.value for a in PicamConstraintSeverity}
drPicamConstraintSeverity={a.value:a.name for a in PicamConstraintSeverity}


class PicamConstraintCategory(enum.IntEnum):
    PicamConstraintCategory_Capable    =_int32(1)
    PicamConstraintCategory_Required   =_int32(2)
    PicamConstraintCategory_Recommended=_int32(3)
dPicamConstraintCategory={a.name:a.value for a in PicamConstraintCategory}
drPicamConstraintCategory={a.value:a.name for a in PicamConstraintCategory}


class PicamCollectionConstraint(ctypes.Structure):
    _fields_=[  ("scope",ctypes.c_int),
                ("severity",ctypes.c_int),
                ("values_array",ctypes.POINTER(piflt)),
                ("values_count",piint) ]
PPicamCollectionConstraint=ctypes.POINTER(PicamCollectionConstraint)
class CPicamCollectionConstraint(ctypes_wrap.CStructWrapper):
    _struct=PicamCollectionConstraint


class PicamRangeConstraint(ctypes.Structure):
    _fields_=[  ("scope",ctypes.c_int),
                ("severity",ctypes.c_int),
                ("empty_set",pibln),
                ("minimum",piflt),
                ("maximum",piflt),
                ("increment",piflt),
                ("excluded_values_array",ctypes.POINTER(piflt)),
                ("excluded_values_count",piint),
                ("outlying_values_array",ctypes.POINTER(piflt)),
                ("outlying_values_count",piint) ]
PPicamRangeConstraint=ctypes.POINTER(PicamRangeConstraint)
class CPicamRangeConstraint(ctypes_wrap.CStructWrapper):
    _struct=PicamRangeConstraint


class PicamRoisConstraintRulesMask(enum.IntEnum):
    PicamRoisConstraintRulesMask_None                 =_int32(0x00)
    PicamRoisConstraintRulesMask_XBinningAlignment    =_int32(0x01)
    PicamRoisConstraintRulesMask_YBinningAlignment    =_int32(0x02)
    PicamRoisConstraintRulesMask_HorizontalSymmetry   =_int32(0x04)
    PicamRoisConstraintRulesMask_VerticalSymmetry     =_int32(0x08)
    PicamRoisConstraintRulesMask_SymmetryBoundsBinning=_int32(0x10)
dPicamRoisConstraintRulesMask={a.name:a.value for a in PicamRoisConstraintRulesMask}
drPicamRoisConstraintRulesMask={a.value:a.name for a in PicamRoisConstraintRulesMask}


class PicamRoisConstraint(ctypes.Structure):
    _fields_=[  ("scope",ctypes.c_int),
                ("severity",ctypes.c_int),
                ("empty_set",pibln),
                ("rules",ctypes.c_int),
                ("maximum_roi_count",piint),
                ("x_constraint",PicamRangeConstraint),
                ("width_constraint",PicamRangeConstraint),
                ("x_binning_limits_array",ctypes.POINTER(piint)),
                ("x_binning_limits_count",piint),
                ("y_constraint",PicamRangeConstraint),
                ("height_constraint",PicamRangeConstraint),
                ("y_binning_limits_array",ctypes.POINTER(piint)),
                ("y_binning_limits_count",piint) ]
PPicamRoisConstraint=ctypes.POINTER(PicamRoisConstraint)
class CPicamRoisConstraint(ctypes_wrap.CStructWrapper):
    _struct=PicamRoisConstraint


class PicamPulseConstraint(ctypes.Structure):
    _fields_=[  ("scope",ctypes.c_int),
                ("severity",ctypes.c_int),
                ("empty_set",pibln),
                ("delay_constraint",PicamRangeConstraint),
                ("width_constraint",PicamRangeConstraint),
                ("minimum_duration",piflt),
                ("maximum_duration",piflt) ]
PPicamPulseConstraint=ctypes.POINTER(PicamPulseConstraint)
class CPicamPulseConstraint(ctypes_wrap.CStructWrapper):
    _struct=PicamPulseConstraint


class PicamModulationsConstraint(ctypes.Structure):
    _fields_=[  ("scope",ctypes.c_int),
                ("severity",ctypes.c_int),
                ("empty_set",pibln),
                ("maximum_modulation_count",piint),
                ("duration_constraint",PicamRangeConstraint),
                ("frequency_constraint",PicamRangeConstraint),
                ("phase_constraint",PicamRangeConstraint),
                ("output_signal_frequency_constraint",PicamRangeConstraint) ]
PPicamModulationsConstraint=ctypes.POINTER(PicamModulationsConstraint)
class CPicamModulationsConstraint(ctypes_wrap.CStructWrapper):
    _struct=PicamModulationsConstraint


class PicamAvailableData(ctypes.Structure):
    _fields_=[  ("initial_readout",ctypes.c_void_p),
                ("readout_count",pi64s) ]
PPicamAvailableData=ctypes.POINTER(PicamAvailableData)
class CPicamAvailableData(ctypes_wrap.CStructWrapper):
    _struct=PicamAvailableData


class PicamAcquisitionErrorsMask(enum.IntEnum):
    PicamAcquisitionErrorsMask_None             =_int32(0x00)
    PicamAcquisitionErrorsMask_CameraFaulted    =_int32(0x10)
    PicamAcquisitionErrorsMask_ConnectionLost   =_int32(0x02)
    PicamAcquisitionErrorsMask_ShutterOverheated=_int32(0x08)
    PicamAcquisitionErrorsMask_DataLost         =_int32(0x01)
    PicamAcquisitionErrorsMask_DataNotArriving  =_int32(0x04)
dPicamAcquisitionErrorsMask={a.name:a.value for a in PicamAcquisitionErrorsMask}
drPicamAcquisitionErrorsMask={a.value:a.name for a in PicamAcquisitionErrorsMask}


class PicamAcquisitionStatus(ctypes.Structure):
    _fields_=[  ("running",pibln),
                ("errors",ctypes.c_int),
                ("readout_rate",piflt) ]
PPicamAcquisitionStatus=ctypes.POINTER(PicamAcquisitionStatus)
class CPicamAcquisitionStatus(ctypes_wrap.CStructWrapper):
    _struct=PicamAcquisitionStatus


class PicamDiscoveryAction(enum.IntEnum):
    PicamDiscoveryAction_Found  =_int32(1)
    PicamDiscoveryAction_Lost   =_int32(2)
    PicamDiscoveryAction_Faulted=_int32(3)
dPicamDiscoveryAction={a.name:a.value for a in PicamDiscoveryAction}
drPicamDiscoveryAction={a.value:a.name for a in PicamDiscoveryAction}


PicamDiscoveryCallback=ctypes.c_void_p
class PicamHandleType(enum.IntEnum):
    PicamHandleType_CameraDevice =_int32(1)
    PicamHandleType_CameraModel  =_int32(2)
    PicamHandleType_Accessory    =_int32(4)
    PicamHandleType_EMCalibration=_int32(3)
dPicamHandleType={a.name:a.value for a in PicamHandleType}
drPicamHandleType={a.value:a.name for a in PicamHandleType}


class PicamPixelLocation(ctypes.Structure):
    _fields_=[  ("x",pi16s),
                ("y",pi16s) ]
PPicamPixelLocation=ctypes.POINTER(PicamPixelLocation)
class CPicamPixelLocation(ctypes_wrap.CStructWrapper):
    _struct=PicamPixelLocation


class PicamColumnDefect(ctypes.Structure):
    _fields_=[  ("start",PicamPixelLocation),
                ("height",piint) ]
PPicamColumnDefect=ctypes.POINTER(PicamColumnDefect)
class CPicamColumnDefect(ctypes_wrap.CStructWrapper):
    _struct=PicamColumnDefect


class PicamRowDefect(ctypes.Structure):
    _fields_=[  ("start",PicamPixelLocation),
                ("width",piint) ]
PPicamRowDefect=ctypes.POINTER(PicamRowDefect)
class CPicamRowDefect(ctypes_wrap.CStructWrapper):
    _struct=PicamRowDefect


class PicamPixelDefectMap(ctypes.Structure):
    _fields_=[  ("column_defect_array",ctypes.POINTER(PicamColumnDefect)),
                ("column_defect_count",piint),
                ("row_defect_array",ctypes.POINTER(PicamRowDefect)),
                ("row_defect_count",piint),
                ("point_defect_array",ctypes.POINTER(PicamPixelLocation)),
                ("point_defect_count",piint) ]
PPicamPixelDefectMap=ctypes.POINTER(PicamPixelDefectMap)
class CPicamPixelDefectMap(ctypes_wrap.CStructWrapper):
    _struct=PicamPixelDefectMap


class PicamStarDefect(ctypes.Structure):
    _fields_=[  ("center",PicamPixelLocation),
                ("bias",pi32f),
                ("adjacent_factor",pi32f),
                ("diagonal_factor",pi32f) ]
PPicamStarDefect=ctypes.POINTER(PicamStarDefect)
class CPicamStarDefect(ctypes_wrap.CStructWrapper):
    _struct=PicamStarDefect


class PicamStarDefectMap(ctypes.Structure):
    _fields_=[  ("id",piint),
                ("star_defect_array",ctypes.POINTER(PicamStarDefect)),
                ("star_defect_count",piint) ]
PPicamStarDefectMap=ctypes.POINTER(PicamStarDefectMap)
class CPicamStarDefectMap(ctypes_wrap.CStructWrapper):
    _struct=PicamStarDefectMap


PicamIntegerValueChangedCallback=ctypes.c_void_p
PicamLargeIntegerValueChangedCallback=ctypes.c_void_p
PicamFloatingPointValueChangedCallback=ctypes.c_void_p
PicamRoisValueChangedCallback=ctypes.c_void_p
PicamPulseValueChangedCallback=ctypes.c_void_p
PicamModulationsValueChangedCallback=ctypes.c_void_p
PicamWhenStatusParameterValueCallback=ctypes.c_void_p
PicamIsRelevantChangedCallback=ctypes.c_void_p
PicamValueAccessChangedCallback=ctypes.c_void_p
class PicamDynamicsMask(enum.IntEnum):
    PicamDynamicsMask_None       =_int32(0x0)
    PicamDynamicsMask_Value      =_int32(0x1)
    PicamDynamicsMask_ValueAccess=_int32(0x2)
    PicamDynamicsMask_IsRelevant =_int32(0x4)
    PicamDynamicsMask_Constraint =_int32(0x8)
dPicamDynamicsMask={a.name:a.value for a in PicamDynamicsMask}
drPicamDynamicsMask={a.value:a.name for a in PicamDynamicsMask}


PicamDependentCollectionConstraintChangedCallback=ctypes.c_void_p
PicamDependentRangeConstraintChangedCallback=ctypes.c_void_p
PicamDependentRoisConstraintChangedCallback=ctypes.c_void_p
PicamDependentPulseConstraintChangedCallback=ctypes.c_void_p
PicamDependentModulationsConstraintChangedCallback=ctypes.c_void_p
class PicamValidationResult(ctypes.Structure):
    _fields_=[  ("is_valid",pibln),
                ("failed_parameter",ctypes.POINTER(ctypes.c_int)),
                ("failed_error_constraint_scope",ctypes.POINTER(ctypes.c_int)),
                ("failed_warning_constraint_scope",ctypes.POINTER(ctypes.c_int)),
                ("error_constraining_parameter_array",ctypes.POINTER(ctypes.c_int)),
                ("error_constraining_parameter_count",piint),
                ("warning_constraining_parameter_array",ctypes.POINTER(ctypes.c_int)),
                ("warning_constraining_parameter_count",piint) ]
PPicamValidationResult=ctypes.POINTER(PicamValidationResult)
class CPicamValidationResult(ctypes_wrap.CStructWrapper):
    _struct=PicamValidationResult


class PicamValidationResults(ctypes.Structure):
    _fields_=[  ("is_valid",pibln),
                ("validation_result_array",ctypes.POINTER(PicamValidationResult)),
                ("validation_result_count",piint) ]
PPicamValidationResults=ctypes.POINTER(PicamValidationResults)
class CPicamValidationResults(ctypes_wrap.CStructWrapper):
    _struct=PicamValidationResults


class PicamFailedDependentParameter(ctypes.Structure):
    _fields_=[  ("failed_parameter",ctypes.c_int),
                ("failed_error_constraint_scope",ctypes.POINTER(ctypes.c_int)),
                ("failed_warning_constraint_scope",ctypes.POINTER(ctypes.c_int)) ]
PPicamFailedDependentParameter=ctypes.POINTER(PicamFailedDependentParameter)
class CPicamFailedDependentParameter(ctypes_wrap.CStructWrapper):
    _struct=PicamFailedDependentParameter


class PicamDependentValidationResult(ctypes.Structure):
    _fields_=[  ("is_valid",pibln),
                ("constraining_parameter",ctypes.c_int),
                ("failed_dependent_parameter_array",ctypes.POINTER(PicamFailedDependentParameter)),
                ("failed_dependent_parameter_count",piint) ]
PPicamDependentValidationResult=ctypes.POINTER(PicamDependentValidationResult)
class CPicamDependentValidationResult(ctypes_wrap.CStructWrapper):
    _struct=PicamDependentValidationResult


class PicamAcquisitionBuffer(ctypes.Structure):
    _fields_=[  ("memory",ctypes.c_void_p),
                ("memory_size",pi64s) ]
PPicamAcquisitionBuffer=ctypes.POINTER(PicamAcquisitionBuffer)
class CPicamAcquisitionBuffer(ctypes_wrap.CStructWrapper):
    _struct=PicamAcquisitionBuffer


PicamAcquisitionUpdatedCallback=ctypes.c_void_p
class PicamAcquisitionState(enum.IntEnum):
    PicamAcquisitionState_ReadoutStarted=_int32(1)
    PicamAcquisitionState_ReadoutEnded  =_int32(2)
dPicamAcquisitionState={a.name:a.value for a in PicamAcquisitionState}
drPicamAcquisitionState={a.value:a.name for a in PicamAcquisitionState}


class PicamAcquisitionStateErrorsMask(enum.IntEnum):
    PicamAcquisitionStateErrorsMask_None     =_int32(0x0)
    PicamAcquisitionStateErrorsMask_LostCount=_int32(0x1)
dPicamAcquisitionStateErrorsMask={a.name:a.value for a in PicamAcquisitionStateErrorsMask}
drPicamAcquisitionStateErrorsMask={a.value:a.name for a in PicamAcquisitionStateErrorsMask}


class PicamAcquisitionStateCounters(ctypes.Structure):
    _fields_=[  ("readout_started_count",pi64s),
                ("readout_ended_count",pi64s) ]
PPicamAcquisitionStateCounters=ctypes.POINTER(PicamAcquisitionStateCounters)
class CPicamAcquisitionStateCounters(ctypes_wrap.CStructWrapper):
    _struct=PicamAcquisitionStateCounters


PicamAcquisitionStateUpdatedCallback=ctypes.c_void_p



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
    #  ctypes.c_int Picam_GetVersion(ctypes.POINTER(piint) major, ctypes.POINTER(piint) minor, ctypes.POINTER(piint) distribution, ctypes.POINTER(piint) released)
    addfunc(lib, "Picam_GetVersion", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(piint), ctypes.POINTER(piint), ctypes.POINTER(piint), ctypes.POINTER(piint)],
            argnames = ["major", "minor", "distribution", "released"] )
    #  ctypes.c_int Picam_IsLibraryInitialized(ctypes.POINTER(pibln) inited)
    addfunc(lib, "Picam_IsLibraryInitialized", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(pibln)],
            argnames = ["inited"] )
    #  ctypes.c_int Picam_InitializeLibrary()
    addfunc(lib, "Picam_InitializeLibrary", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int Picam_UninitializeLibrary()
    addfunc(lib, "Picam_UninitializeLibrary", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int Picam_DestroyString(ctypes.c_char_p s)
    addfunc(lib, "Picam_DestroyString", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p],
            argnames = ["s"] )
    #  ctypes.c_int Picam_GetEnumerationString(ctypes.c_int type, piint value, ctypes.POINTER(ctypes.c_char_p) s)
    addfunc(lib, "Picam_GetEnumerationString", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, piint, ctypes.POINTER(ctypes.c_char_p)],
            argnames = ["type", "value", "s"] )
    #  ctypes.c_int Picam_DestroyCameraIDs(ctypes.POINTER(PicamCameraID) id_array)
    addfunc(lib, "Picam_DestroyCameraIDs", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCameraID)],
            argnames = ["id_array"] )
    #  ctypes.c_int Picam_GetAvailableCameraIDs(ctypes.POINTER(ctypes.POINTER(PicamCameraID)) id_array, ctypes.POINTER(piint) id_count)
    addfunc(lib, "Picam_GetAvailableCameraIDs", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.POINTER(PicamCameraID)), ctypes.POINTER(piint)],
            argnames = ["id_array", "id_count"] )
    #  ctypes.c_int Picam_GetUnavailableCameraIDs(ctypes.POINTER(ctypes.POINTER(PicamCameraID)) id_array, ctypes.POINTER(piint) id_count)
    addfunc(lib, "Picam_GetUnavailableCameraIDs", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.POINTER(PicamCameraID)), ctypes.POINTER(piint)],
            argnames = ["id_array", "id_count"] )
    #  ctypes.c_int Picam_IsCameraIDConnected(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(pibln) connected)
    addfunc(lib, "Picam_IsCameraIDConnected", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCameraID), ctypes.POINTER(pibln)],
            argnames = ["id", "connected"] )
    #  ctypes.c_int Picam_IsCameraIDOpenElsewhere(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(pibln) open_elsewhere)
    addfunc(lib, "Picam_IsCameraIDOpenElsewhere", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCameraID), ctypes.POINTER(pibln)],
            argnames = ["id", "open_elsewhere"] )
    #  ctypes.c_int Picam_DestroyHandles(ctypes.POINTER(PicamHandle) handle_array)
    addfunc(lib, "Picam_DestroyHandles", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamHandle)],
            argnames = ["handle_array"] )
    #  ctypes.c_int Picam_OpenFirstCamera(ctypes.POINTER(PicamHandle) camera)
    addfunc(lib, "Picam_OpenFirstCamera", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamHandle)],
            argnames = ["camera"] )
    #  ctypes.c_int Picam_OpenCamera(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(PicamHandle) camera)
    addfunc(lib, "Picam_OpenCamera", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCameraID), ctypes.POINTER(PicamHandle)],
            argnames = ["id", "camera"] )
    #  ctypes.c_int Picam_CloseCamera(PicamHandle camera)
    addfunc(lib, "Picam_CloseCamera", restype = ctypes.c_int,
            argtypes = [PicamHandle],
            argnames = ["camera"] )
    #  ctypes.c_int Picam_GetOpenCameras(ctypes.POINTER(ctypes.POINTER(PicamHandle)) camera_array, ctypes.POINTER(piint) camera_count)
    addfunc(lib, "Picam_GetOpenCameras", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.POINTER(PicamHandle)), ctypes.POINTER(piint)],
            argnames = ["camera_array", "camera_count"] )
    #  ctypes.c_int Picam_IsCameraConnected(PicamHandle camera, ctypes.POINTER(pibln) connected)
    addfunc(lib, "Picam_IsCameraConnected", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(pibln)],
            argnames = ["camera", "connected"] )
    #  ctypes.c_int Picam_IsCameraFaulted(PicamHandle camera, ctypes.POINTER(pibln) faulted)
    addfunc(lib, "Picam_IsCameraFaulted", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(pibln)],
            argnames = ["camera", "faulted"] )
    #  ctypes.c_int Picam_GetCameraID(PicamHandle camera, ctypes.POINTER(PicamCameraID) id)
    addfunc(lib, "Picam_GetCameraID", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(PicamCameraID)],
            argnames = ["camera", "id"] )
    #  ctypes.c_int Picam_DestroyFirmwareDetails(ctypes.POINTER(PicamFirmwareDetail) firmware_array)
    addfunc(lib, "Picam_DestroyFirmwareDetails", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamFirmwareDetail)],
            argnames = ["firmware_array"] )
    #  ctypes.c_int Picam_GetFirmwareDetails(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(ctypes.POINTER(PicamFirmwareDetail)) firmware_array, ctypes.POINTER(piint) firmware_count)
    addfunc(lib, "Picam_GetFirmwareDetails", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCameraID), ctypes.POINTER(ctypes.POINTER(PicamFirmwareDetail)), ctypes.POINTER(piint)],
            argnames = ["id", "firmware_array", "firmware_count"] )
    #  ctypes.c_int Picam_DestroyCalibrations(ctypes.POINTER(PicamCalibration) calibration_array)
    addfunc(lib, "Picam_DestroyCalibrations", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCalibration)],
            argnames = ["calibration_array"] )
    #  ctypes.c_int Picam_DestroyModels(ctypes.POINTER(ctypes.c_int) model_array)
    addfunc(lib, "Picam_DestroyModels", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["model_array"] )
    #  ctypes.c_int Picam_GetAvailableDemoCameraModels(ctypes.POINTER(ctypes.POINTER(ctypes.c_int)) model_array, ctypes.POINTER(piint) model_count)
    addfunc(lib, "Picam_GetAvailableDemoCameraModels", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(piint)],
            argnames = ["model_array", "model_count"] )
    #  ctypes.c_int Picam_ConnectDemoCamera(ctypes.c_int model, ctypes.c_char_p serial_number, ctypes.POINTER(PicamCameraID) id)
    addfunc(lib, "Picam_ConnectDemoCamera", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(PicamCameraID)],
            argnames = ["model", "serial_number", "id"] )
    #  ctypes.c_int Picam_DisconnectDemoCamera(ctypes.POINTER(PicamCameraID) id)
    addfunc(lib, "Picam_DisconnectDemoCamera", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCameraID)],
            argnames = ["id"] )
    #  ctypes.c_int Picam_IsDemoCamera(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(pibln) demo)
    addfunc(lib, "Picam_IsDemoCamera", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCameraID), ctypes.POINTER(pibln)],
            argnames = ["id", "demo"] )
    #  ctypes.c_int Picam_GetParameterIntegerValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piint) value)
    addfunc(lib, "Picam_GetParameterIntegerValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(piint)],
            argnames = ["camera_or_accessory", "parameter", "value"] )
    #  ctypes.c_int Picam_SetParameterIntegerValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piint value)
    addfunc(lib, "Picam_SetParameterIntegerValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piint],
            argnames = ["camera_or_accessory", "parameter", "value"] )
    #  ctypes.c_int Picam_CanSetParameterIntegerValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piint value, ctypes.POINTER(pibln) settable)
    addfunc(lib, "Picam_CanSetParameterIntegerValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piint, ctypes.POINTER(pibln)],
            argnames = ["camera_or_accessory", "parameter", "value", "settable"] )
    #  ctypes.c_int Picam_GetParameterLargeIntegerValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(pi64s) value)
    addfunc(lib, "Picam_GetParameterLargeIntegerValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(pi64s)],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_SetParameterLargeIntegerValue(PicamHandle camera, ctypes.c_int parameter, pi64s value)
    addfunc(lib, "Picam_SetParameterLargeIntegerValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, pi64s],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_CanSetParameterLargeIntegerValue(PicamHandle camera, ctypes.c_int parameter, pi64s value, ctypes.POINTER(pibln) settable)
    addfunc(lib, "Picam_CanSetParameterLargeIntegerValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, pi64s, ctypes.POINTER(pibln)],
            argnames = ["camera", "parameter", "value", "settable"] )
    #  ctypes.c_int Picam_GetParameterFloatingPointValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piflt) value)
    addfunc(lib, "Picam_GetParameterFloatingPointValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(piflt)],
            argnames = ["camera_or_accessory", "parameter", "value"] )
    #  ctypes.c_int Picam_SetParameterFloatingPointValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piflt value)
    addfunc(lib, "Picam_SetParameterFloatingPointValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piflt],
            argnames = ["camera_or_accessory", "parameter", "value"] )
    #  ctypes.c_int Picam_CanSetParameterFloatingPointValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piflt value, ctypes.POINTER(pibln) settable)
    addfunc(lib, "Picam_CanSetParameterFloatingPointValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piflt, ctypes.POINTER(pibln)],
            argnames = ["camera_or_accessory", "parameter", "value", "settable"] )
    #  ctypes.c_int Picam_DestroyRois(ctypes.POINTER(PicamRois) rois)
    addfunc(lib, "Picam_DestroyRois", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamRois)],
            argnames = ["rois"] )
    #  ctypes.c_int Picam_GetParameterRoisValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamRois)) value)
    addfunc(lib, "Picam_GetParameterRoisValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamRois))],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_SetParameterRoisValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamRois) value)
    addfunc(lib, "Picam_SetParameterRoisValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(PicamRois)],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_CanSetParameterRoisValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamRois) value, ctypes.POINTER(pibln) settable)
    addfunc(lib, "Picam_CanSetParameterRoisValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(PicamRois), ctypes.POINTER(pibln)],
            argnames = ["camera", "parameter", "value", "settable"] )
    #  ctypes.c_int Picam_DestroyPulses(ctypes.POINTER(PicamPulse) pulses)
    addfunc(lib, "Picam_DestroyPulses", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamPulse)],
            argnames = ["pulses"] )
    #  ctypes.c_int Picam_GetParameterPulseValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamPulse)) value)
    addfunc(lib, "Picam_GetParameterPulseValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamPulse))],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_SetParameterPulseValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamPulse) value)
    addfunc(lib, "Picam_SetParameterPulseValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(PicamPulse)],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_CanSetParameterPulseValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamPulse) value, ctypes.POINTER(pibln) settable)
    addfunc(lib, "Picam_CanSetParameterPulseValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(PicamPulse), ctypes.POINTER(pibln)],
            argnames = ["camera", "parameter", "value", "settable"] )
    #  ctypes.c_int Picam_DestroyModulations(ctypes.POINTER(PicamModulations) modulations)
    addfunc(lib, "Picam_DestroyModulations", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamModulations)],
            argnames = ["modulations"] )
    #  ctypes.c_int Picam_GetParameterModulationsValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamModulations)) value)
    addfunc(lib, "Picam_GetParameterModulationsValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamModulations))],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_SetParameterModulationsValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamModulations) value)
    addfunc(lib, "Picam_SetParameterModulationsValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(PicamModulations)],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_CanSetParameterModulationsValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamModulations) value, ctypes.POINTER(pibln) settable)
    addfunc(lib, "Picam_CanSetParameterModulationsValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(PicamModulations), ctypes.POINTER(pibln)],
            argnames = ["camera", "parameter", "value", "settable"] )
    #  ctypes.c_int Picam_GetParameterIntegerDefaultValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piint) value)
    addfunc(lib, "Picam_GetParameterIntegerDefaultValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(piint)],
            argnames = ["camera_or_accessory", "parameter", "value"] )
    #  ctypes.c_int Picam_GetParameterLargeIntegerDefaultValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(pi64s) value)
    addfunc(lib, "Picam_GetParameterLargeIntegerDefaultValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(pi64s)],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_GetParameterFloatingPointDefaultValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piflt) value)
    addfunc(lib, "Picam_GetParameterFloatingPointDefaultValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(piflt)],
            argnames = ["camera_or_accessory", "parameter", "value"] )
    #  ctypes.c_int Picam_GetParameterRoisDefaultValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamRois)) value)
    addfunc(lib, "Picam_GetParameterRoisDefaultValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamRois))],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_GetParameterPulseDefaultValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamPulse)) value)
    addfunc(lib, "Picam_GetParameterPulseDefaultValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamPulse))],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_GetParameterModulationsDefaultValue(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamModulations)) value)
    addfunc(lib, "Picam_GetParameterModulationsDefaultValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamModulations))],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_RestoreParametersToDefaultValues(PicamHandle camera_or_accessory)
    addfunc(lib, "Picam_RestoreParametersToDefaultValues", restype = ctypes.c_int,
            argtypes = [PicamHandle],
            argnames = ["camera_or_accessory"] )
    #  ctypes.c_int Picam_CanSetParameterOnline(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) onlineable)
    addfunc(lib, "Picam_CanSetParameterOnline", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(pibln)],
            argnames = ["camera_or_accessory", "parameter", "onlineable"] )
    #  ctypes.c_int Picam_SetParameterIntegerValueOnline(PicamHandle camera, ctypes.c_int parameter, piint value)
    addfunc(lib, "Picam_SetParameterIntegerValueOnline", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piint],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_SetParameterFloatingPointValueOnline(PicamHandle camera, ctypes.c_int parameter, piflt value)
    addfunc(lib, "Picam_SetParameterFloatingPointValueOnline", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piflt],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_SetParameterPulseValueOnline(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(PicamPulse) value)
    addfunc(lib, "Picam_SetParameterPulseValueOnline", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(PicamPulse)],
            argnames = ["camera", "parameter", "value"] )
    #  ctypes.c_int Picam_CanReadParameter(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) readable)
    addfunc(lib, "Picam_CanReadParameter", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(pibln)],
            argnames = ["camera_or_accessory", "parameter", "readable"] )
    #  ctypes.c_int Picam_ReadParameterIntegerValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piint) value)
    addfunc(lib, "Picam_ReadParameterIntegerValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(piint)],
            argnames = ["camera_or_accessory", "parameter", "value"] )
    #  ctypes.c_int Picam_ReadParameterFloatingPointValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(piflt) value)
    addfunc(lib, "Picam_ReadParameterFloatingPointValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(piflt)],
            argnames = ["camera_or_accessory", "parameter", "value"] )
    #  ctypes.c_int Picam_CanWaitForStatusParameter(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) waitable)
    addfunc(lib, "Picam_CanWaitForStatusParameter", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(pibln)],
            argnames = ["camera_or_accessory", "parameter", "waitable"] )
    #  ctypes.c_int Picam_DestroyStatusPurviews(ctypes.POINTER(PicamStatusPurview) purviews_array)
    addfunc(lib, "Picam_DestroyStatusPurviews", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamStatusPurview)],
            argnames = ["purviews_array"] )
    #  ctypes.c_int Picam_GetStatusParameterPurview(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamStatusPurview)) purview)
    addfunc(lib, "Picam_GetStatusParameterPurview", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamStatusPurview))],
            argnames = ["camera_or_accessory", "parameter", "purview"] )
    #  ctypes.c_int Picam_EstimateTimeToStatusParameterValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piint value, ctypes.POINTER(piint) estimated_time)
    addfunc(lib, "Picam_EstimateTimeToStatusParameterValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piint, ctypes.POINTER(piint)],
            argnames = ["camera_or_accessory", "parameter", "value", "estimated_time"] )
    #  ctypes.c_int Picam_WaitForStatusParameterValue(PicamHandle camera_or_accessory, ctypes.c_int parameter, piint value, piint time_out)
    addfunc(lib, "Picam_WaitForStatusParameterValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piint, piint],
            argnames = ["camera_or_accessory", "parameter", "value", "time_out"] )
    #  ctypes.c_int Picam_DestroyParameters(ctypes.POINTER(ctypes.c_int) parameter_array)
    addfunc(lib, "Picam_DestroyParameters", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["parameter_array"] )
    #  ctypes.c_int Picam_GetParameters(PicamHandle camera_or_accessory, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)) parameter_array, ctypes.POINTER(piint) parameter_count)
    addfunc(lib, "Picam_GetParameters", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(piint)],
            argnames = ["camera_or_accessory", "parameter_array", "parameter_count"] )
    #  ctypes.c_int Picam_DoesParameterExist(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) exists)
    addfunc(lib, "Picam_DoesParameterExist", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(pibln)],
            argnames = ["camera_or_accessory", "parameter", "exists"] )
    #  ctypes.c_int Picam_IsParameterRelevant(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(pibln) relevant)
    addfunc(lib, "Picam_IsParameterRelevant", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(pibln)],
            argnames = ["camera_or_accessory", "parameter", "relevant"] )
    #  ctypes.c_int Picam_GetParameterValueType(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) type)
    addfunc(lib, "Picam_GetParameterValueType", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["camera_or_accessory", "parameter", "type"] )
    #  ctypes.c_int Picam_GetParameterEnumeratedType(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) type)
    addfunc(lib, "Picam_GetParameterEnumeratedType", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["camera_or_accessory", "parameter", "type"] )
    #  ctypes.c_int Picam_GetParameterValueAccess(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) access)
    addfunc(lib, "Picam_GetParameterValueAccess", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["camera_or_accessory", "parameter", "access"] )
    #  ctypes.c_int Picam_GetParameterConstraintType(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) type)
    addfunc(lib, "Picam_GetParameterConstraintType", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["camera_or_accessory", "parameter", "type"] )
    #  ctypes.c_int Picam_DestroyCollectionConstraints(ctypes.POINTER(PicamCollectionConstraint) constraint_array)
    addfunc(lib, "Picam_DestroyCollectionConstraints", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCollectionConstraint)],
            argnames = ["constraint_array"] )
    #  ctypes.c_int Picam_GetParameterCollectionConstraint(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.c_int category, ctypes.POINTER(ctypes.POINTER(PicamCollectionConstraint)) constraint)
    addfunc(lib, "Picam_GetParameterCollectionConstraint", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamCollectionConstraint))],
            argnames = ["camera_or_accessory", "parameter", "category", "constraint"] )
    #  ctypes.c_int Picam_DestroyRangeConstraints(ctypes.POINTER(PicamRangeConstraint) constraint_array)
    addfunc(lib, "Picam_DestroyRangeConstraints", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamRangeConstraint)],
            argnames = ["constraint_array"] )
    #  ctypes.c_int Picam_GetParameterRangeConstraint(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.c_int category, ctypes.POINTER(ctypes.POINTER(PicamRangeConstraint)) constraint)
    addfunc(lib, "Picam_GetParameterRangeConstraint", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamRangeConstraint))],
            argnames = ["camera_or_accessory", "parameter", "category", "constraint"] )
    #  ctypes.c_int Picam_DestroyRoisConstraints(ctypes.POINTER(PicamRoisConstraint) constraint_array)
    addfunc(lib, "Picam_DestroyRoisConstraints", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamRoisConstraint)],
            argnames = ["constraint_array"] )
    #  ctypes.c_int Picam_GetParameterRoisConstraint(PicamHandle camera, ctypes.c_int parameter, ctypes.c_int category, ctypes.POINTER(ctypes.POINTER(PicamRoisConstraint)) constraint)
    addfunc(lib, "Picam_GetParameterRoisConstraint", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamRoisConstraint))],
            argnames = ["camera", "parameter", "category", "constraint"] )
    #  ctypes.c_int Picam_DestroyPulseConstraints(ctypes.POINTER(PicamPulseConstraint) constraint_array)
    addfunc(lib, "Picam_DestroyPulseConstraints", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamPulseConstraint)],
            argnames = ["constraint_array"] )
    #  ctypes.c_int Picam_GetParameterPulseConstraint(PicamHandle camera, ctypes.c_int parameter, ctypes.c_int category, ctypes.POINTER(ctypes.POINTER(PicamPulseConstraint)) constraint)
    addfunc(lib, "Picam_GetParameterPulseConstraint", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamPulseConstraint))],
            argnames = ["camera", "parameter", "category", "constraint"] )
    #  ctypes.c_int Picam_DestroyModulationsConstraints(ctypes.POINTER(PicamModulationsConstraint) constraint_array)
    addfunc(lib, "Picam_DestroyModulationsConstraints", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamModulationsConstraint)],
            argnames = ["constraint_array"] )
    #  ctypes.c_int Picam_GetParameterModulationsConstraint(PicamHandle camera, ctypes.c_int parameter, ctypes.c_int category, ctypes.POINTER(ctypes.POINTER(PicamModulationsConstraint)) constraint)
    addfunc(lib, "Picam_GetParameterModulationsConstraint", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamModulationsConstraint))],
            argnames = ["camera", "parameter", "category", "constraint"] )
    #  ctypes.c_int Picam_AreParametersCommitted(PicamHandle camera_or_accessory, ctypes.POINTER(pibln) committed)
    addfunc(lib, "Picam_AreParametersCommitted", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(pibln)],
            argnames = ["camera_or_accessory", "committed"] )
    #  ctypes.c_int Picam_CommitParameters(PicamHandle camera_or_accessory, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)) failed_parameter_array, ctypes.POINTER(piint) failed_parameter_count)
    addfunc(lib, "Picam_CommitParameters", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(piint)],
            argnames = ["camera_or_accessory", "failed_parameter_array", "failed_parameter_count"] )
    #  ctypes.c_int Picam_Acquire(PicamHandle camera, pi64s readout_count, piint readout_time_out, ctypes.POINTER(PicamAvailableData) available, ctypes.POINTER(ctypes.c_int) errors)
    addfunc(lib, "Picam_Acquire", restype = ctypes.c_int,
            argtypes = [PicamHandle, pi64s, piint, ctypes.POINTER(PicamAvailableData), ctypes.POINTER(ctypes.c_int)],
            argnames = ["camera", "readout_count", "readout_time_out", "available", "errors"] )
    #  ctypes.c_int Picam_StartAcquisition(PicamHandle camera)
    addfunc(lib, "Picam_StartAcquisition", restype = ctypes.c_int,
            argtypes = [PicamHandle],
            argnames = ["camera"] )
    #  ctypes.c_int Picam_StopAcquisition(PicamHandle camera)
    addfunc(lib, "Picam_StopAcquisition", restype = ctypes.c_int,
            argtypes = [PicamHandle],
            argnames = ["camera"] )
    #  ctypes.c_int Picam_IsAcquisitionRunning(PicamHandle camera, ctypes.POINTER(pibln) running)
    addfunc(lib, "Picam_IsAcquisitionRunning", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(pibln)],
            argnames = ["camera", "running"] )
    #  ctypes.c_int Picam_WaitForAcquisitionUpdate(PicamHandle camera, piint readout_time_out, ctypes.POINTER(PicamAvailableData) available, ctypes.POINTER(PicamAcquisitionStatus) status)
    addfunc(lib, "Picam_WaitForAcquisitionUpdate", restype = ctypes.c_int,
            argtypes = [PicamHandle, piint, ctypes.POINTER(PicamAvailableData), ctypes.POINTER(PicamAcquisitionStatus)],
            argnames = ["camera", "readout_time_out", "available", "status"] )
    #  ctypes.c_int PicamAdvanced_RegisterForDiscovery(PicamDiscoveryCallback discover)
    addfunc(lib, "PicamAdvanced_RegisterForDiscovery", restype = ctypes.c_int,
            argtypes = [PicamDiscoveryCallback],
            argnames = ["discover"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForDiscovery(PicamDiscoveryCallback discover)
    addfunc(lib, "PicamAdvanced_UnregisterForDiscovery", restype = ctypes.c_int,
            argtypes = [PicamDiscoveryCallback],
            argnames = ["discover"] )
    #  ctypes.c_int PicamAdvanced_DiscoverCameras()
    addfunc(lib, "PicamAdvanced_DiscoverCameras", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int PicamAdvanced_StopDiscoveringCameras()
    addfunc(lib, "PicamAdvanced_StopDiscoveringCameras", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int PicamAdvanced_IsDiscoveringCameras(ctypes.POINTER(pibln) discovering)
    addfunc(lib, "PicamAdvanced_IsDiscoveringCameras", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(pibln)],
            argnames = ["discovering"] )
    #  ctypes.c_int PicamAdvanced_GetHandleType(PicamHandle handle, ctypes.POINTER(ctypes.c_int) type)
    addfunc(lib, "PicamAdvanced_GetHandleType", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(ctypes.c_int)],
            argnames = ["handle", "type"] )
    #  ctypes.c_int PicamAdvanced_OpenCameraDevice(ctypes.POINTER(PicamCameraID) id, ctypes.POINTER(PicamHandle) device)
    addfunc(lib, "PicamAdvanced_OpenCameraDevice", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamCameraID), ctypes.POINTER(PicamHandle)],
            argnames = ["id", "device"] )
    #  ctypes.c_int PicamAdvanced_CloseCameraDevice(PicamHandle device)
    addfunc(lib, "PicamAdvanced_CloseCameraDevice", restype = ctypes.c_int,
            argtypes = [PicamHandle],
            argnames = ["device"] )
    #  ctypes.c_int PicamAdvanced_GetOpenCameraDevices(ctypes.POINTER(ctypes.POINTER(PicamHandle)) device_array, ctypes.POINTER(piint) device_count)
    addfunc(lib, "PicamAdvanced_GetOpenCameraDevices", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.POINTER(PicamHandle)), ctypes.POINTER(piint)],
            argnames = ["device_array", "device_count"] )
    #  ctypes.c_int PicamAdvanced_GetCameraModel(PicamHandle camera, ctypes.POINTER(PicamHandle) model)
    addfunc(lib, "PicamAdvanced_GetCameraModel", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(PicamHandle)],
            argnames = ["camera", "model"] )
    #  ctypes.c_int PicamAdvanced_GetCameraDevice(PicamHandle camera, ctypes.POINTER(PicamHandle) device)
    addfunc(lib, "PicamAdvanced_GetCameraDevice", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(PicamHandle)],
            argnames = ["camera", "device"] )
    #  ctypes.c_int PicamAdvanced_GetUserState(PicamHandle camera_or_accessory, ctypes.POINTER(ctypes.c_void_p) user_state)
    addfunc(lib, "PicamAdvanced_GetUserState", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(ctypes.c_void_p)],
            argnames = ["camera_or_accessory", "user_state"] )
    #  ctypes.c_int PicamAdvanced_SetUserState(PicamHandle camera_or_accessory, ctypes.c_void_p user_state)
    addfunc(lib, "PicamAdvanced_SetUserState", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_void_p],
            argnames = ["camera_or_accessory", "user_state"] )
    #  ctypes.c_int PicamAdvanced_DestroyPixelDefectMaps(ctypes.POINTER(PicamPixelDefectMap) pixel_defect_map_array)
    addfunc(lib, "PicamAdvanced_DestroyPixelDefectMaps", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamPixelDefectMap)],
            argnames = ["pixel_defect_map_array"] )
    #  ctypes.c_int PicamAdvanced_GetPixelDefectMap(PicamHandle camera, ctypes.POINTER(ctypes.POINTER(PicamPixelDefectMap)) pixel_defect_map)
    addfunc(lib, "PicamAdvanced_GetPixelDefectMap", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(ctypes.POINTER(PicamPixelDefectMap))],
            argnames = ["camera", "pixel_defect_map"] )
    #  ctypes.c_int PicamAdvanced_DestroyStarDefectMaps(ctypes.POINTER(PicamStarDefectMap) star_defect_map_array)
    addfunc(lib, "PicamAdvanced_DestroyStarDefectMaps", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamStarDefectMap)],
            argnames = ["star_defect_map_array"] )
    #  ctypes.c_int PicamAdvanced_GetStarDefectMap(PicamHandle camera, ctypes.POINTER(ctypes.POINTER(PicamStarDefectMap)) star_defect_map)
    addfunc(lib, "PicamAdvanced_GetStarDefectMap", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(ctypes.POINTER(PicamStarDefectMap))],
            argnames = ["camera", "star_defect_map"] )
    #  ctypes.c_int PicamAdvanced_GetStarDefectMaps(PicamHandle camera, ctypes.POINTER(ctypes.POINTER(PicamStarDefectMap)) star_defect_map_array, ctypes.POINTER(piint) star_defect_map_count)
    addfunc(lib, "PicamAdvanced_GetStarDefectMaps", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(ctypes.POINTER(PicamStarDefectMap)), ctypes.POINTER(piint)],
            argnames = ["camera", "star_defect_map_array", "star_defect_map_count"] )
    #  ctypes.c_int PicamAdvanced_RegisterForIntegerValueChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamIntegerValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForIntegerValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamIntegerValueChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForIntegerValueChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamIntegerValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForIntegerValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamIntegerValueChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_RegisterForExtrinsicIntegerValueChanged(PicamHandle device_or_accessory, ctypes.c_int parameter, PicamIntegerValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForExtrinsicIntegerValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamIntegerValueChangedCallback],
            argnames = ["device_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForExtrinsicIntegerValueChanged(PicamHandle device_or_accessory, ctypes.c_int parameter, PicamIntegerValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForExtrinsicIntegerValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamIntegerValueChangedCallback],
            argnames = ["device_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_RegisterForLargeIntegerValueChanged(PicamHandle camera, ctypes.c_int parameter, PicamLargeIntegerValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForLargeIntegerValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamLargeIntegerValueChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForLargeIntegerValueChanged(PicamHandle camera, ctypes.c_int parameter, PicamLargeIntegerValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForLargeIntegerValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamLargeIntegerValueChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_RegisterForFloatingPointValueChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamFloatingPointValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForFloatingPointValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamFloatingPointValueChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForFloatingPointValueChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamFloatingPointValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForFloatingPointValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamFloatingPointValueChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_RegisterForExtrinsicFloatingPointValueChanged(PicamHandle device_or_accessory, ctypes.c_int parameter, PicamFloatingPointValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForExtrinsicFloatingPointValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamFloatingPointValueChangedCallback],
            argnames = ["device_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForExtrinsicFloatingPointValueChanged(PicamHandle device_or_accessory, ctypes.c_int parameter, PicamFloatingPointValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForExtrinsicFloatingPointValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamFloatingPointValueChangedCallback],
            argnames = ["device_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_RegisterForRoisValueChanged(PicamHandle camera, ctypes.c_int parameter, PicamRoisValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForRoisValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamRoisValueChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForRoisValueChanged(PicamHandle camera, ctypes.c_int parameter, PicamRoisValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForRoisValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamRoisValueChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_RegisterForPulseValueChanged(PicamHandle camera, ctypes.c_int parameter, PicamPulseValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForPulseValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamPulseValueChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForPulseValueChanged(PicamHandle camera, ctypes.c_int parameter, PicamPulseValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForPulseValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamPulseValueChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_RegisterForModulationsValueChanged(PicamHandle camera, ctypes.c_int parameter, PicamModulationsValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForModulationsValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamModulationsValueChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForModulationsValueChanged(PicamHandle camera, ctypes.c_int parameter, PicamModulationsValueChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForModulationsValueChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamModulationsValueChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_NotifyWhenStatusParameterValue(PicamHandle device_or_accessory, ctypes.c_int parameter, piint value, PicamWhenStatusParameterValueCallback when)
    addfunc(lib, "PicamAdvanced_NotifyWhenStatusParameterValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piint, PicamWhenStatusParameterValueCallback],
            argnames = ["device_or_accessory", "parameter", "value", "when"] )
    #  ctypes.c_int PicamAdvanced_CancelNotifyWhenStatusParameterValue(PicamHandle device_or_accessory, ctypes.c_int parameter, piint value, PicamWhenStatusParameterValueCallback when)
    addfunc(lib, "PicamAdvanced_CancelNotifyWhenStatusParameterValue", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, piint, PicamWhenStatusParameterValueCallback],
            argnames = ["device_or_accessory", "parameter", "value", "when"] )
    #  ctypes.c_int PicamAdvanced_RegisterForIsRelevantChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamIsRelevantChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForIsRelevantChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamIsRelevantChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForIsRelevantChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamIsRelevantChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForIsRelevantChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamIsRelevantChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_RegisterForValueAccessChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamValueAccessChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForValueAccessChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamValueAccessChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForValueAccessChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamValueAccessChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForValueAccessChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamValueAccessChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_GetParameterDynamics(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) dynamics)
    addfunc(lib, "PicamAdvanced_GetParameterDynamics", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["camera_or_accessory", "parameter", "dynamics"] )
    #  ctypes.c_int PicamAdvanced_GetParameterExtrinsicDynamics(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_int) extrinsic)
    addfunc(lib, "PicamAdvanced_GetParameterExtrinsicDynamics", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["camera_or_accessory", "parameter", "extrinsic"] )
    #  ctypes.c_int PicamAdvanced_GetParameterCollectionConstraints(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamCollectionConstraint)) constraint_array, ctypes.POINTER(piint) constraint_count)
    addfunc(lib, "PicamAdvanced_GetParameterCollectionConstraints", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamCollectionConstraint)), ctypes.POINTER(piint)],
            argnames = ["camera_or_accessory", "parameter", "constraint_array", "constraint_count"] )
    #  ctypes.c_int PicamAdvanced_RegisterForDependentCollectionConstraintChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamDependentCollectionConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForDependentCollectionConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentCollectionConstraintChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForDependentCollectionConstraintChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamDependentCollectionConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForDependentCollectionConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentCollectionConstraintChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_GetParameterRangeConstraints(PicamHandle camera_or_accessory, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamRangeConstraint)) constraint_array, ctypes.POINTER(piint) constraint_count)
    addfunc(lib, "PicamAdvanced_GetParameterRangeConstraints", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamRangeConstraint)), ctypes.POINTER(piint)],
            argnames = ["camera_or_accessory", "parameter", "constraint_array", "constraint_count"] )
    #  ctypes.c_int PicamAdvanced_RegisterForDependentRangeConstraintChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamDependentRangeConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForDependentRangeConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentRangeConstraintChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForDependentRangeConstraintChanged(PicamHandle camera_or_accessory, ctypes.c_int parameter, PicamDependentRangeConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForDependentRangeConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentRangeConstraintChangedCallback],
            argnames = ["camera_or_accessory", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_GetParameterRoisConstraints(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamRoisConstraint)) constraint_array, ctypes.POINTER(piint) constraint_count)
    addfunc(lib, "PicamAdvanced_GetParameterRoisConstraints", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamRoisConstraint)), ctypes.POINTER(piint)],
            argnames = ["camera", "parameter", "constraint_array", "constraint_count"] )
    #  ctypes.c_int PicamAdvanced_RegisterForDependentRoisConstraintChanged(PicamHandle camera, ctypes.c_int parameter, PicamDependentRoisConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForDependentRoisConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentRoisConstraintChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForDependentRoisConstraintChanged(PicamHandle camera, ctypes.c_int parameter, PicamDependentRoisConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForDependentRoisConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentRoisConstraintChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_GetParameterPulseConstraints(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamPulseConstraint)) constraint_array, ctypes.POINTER(piint) constraint_count)
    addfunc(lib, "PicamAdvanced_GetParameterPulseConstraints", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamPulseConstraint)), ctypes.POINTER(piint)],
            argnames = ["camera", "parameter", "constraint_array", "constraint_count"] )
    #  ctypes.c_int PicamAdvanced_RegisterForDependentPulseConstraintChanged(PicamHandle camera, ctypes.c_int parameter, PicamDependentPulseConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForDependentPulseConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentPulseConstraintChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForDependentPulseConstraintChanged(PicamHandle camera, ctypes.c_int parameter, PicamDependentPulseConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForDependentPulseConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentPulseConstraintChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_GetParameterModulationsConstraints(PicamHandle camera, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamModulationsConstraint)) constraint_array, ctypes.POINTER(piint) constraint_count)
    addfunc(lib, "PicamAdvanced_GetParameterModulationsConstraints", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamModulationsConstraint)), ctypes.POINTER(piint)],
            argnames = ["camera", "parameter", "constraint_array", "constraint_count"] )
    #  ctypes.c_int PicamAdvanced_RegisterForDependentModulationsConstraintChanged(PicamHandle camera, ctypes.c_int parameter, PicamDependentModulationsConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_RegisterForDependentModulationsConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentModulationsConstraintChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForDependentModulationsConstraintChanged(PicamHandle camera, ctypes.c_int parameter, PicamDependentModulationsConstraintChangedCallback changed)
    addfunc(lib, "PicamAdvanced_UnregisterForDependentModulationsConstraintChanged", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamDependentModulationsConstraintChangedCallback],
            argnames = ["camera", "parameter", "changed"] )
    #  ctypes.c_int Picam_DestroyValidationResult(ctypes.POINTER(PicamValidationResult) result)
    addfunc(lib, "Picam_DestroyValidationResult", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamValidationResult)],
            argnames = ["result"] )
    #  ctypes.c_int Picam_DestroyValidationResults(ctypes.POINTER(PicamValidationResults) results)
    addfunc(lib, "Picam_DestroyValidationResults", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamValidationResults)],
            argnames = ["results"] )
    #  ctypes.c_int PicamAdvanced_ValidateParameter(PicamHandle model, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamValidationResult)) result)
    addfunc(lib, "PicamAdvanced_ValidateParameter", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamValidationResult))],
            argnames = ["model", "parameter", "result"] )
    #  ctypes.c_int PicamAdvanced_ValidateParameters(PicamHandle model, ctypes.POINTER(ctypes.POINTER(PicamValidationResults)) results)
    addfunc(lib, "PicamAdvanced_ValidateParameters", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(ctypes.POINTER(PicamValidationResults))],
            argnames = ["model", "results"] )
    #  ctypes.c_int Picam_DestroyDependentValidationResult(ctypes.POINTER(PicamDependentValidationResult) result)
    addfunc(lib, "Picam_DestroyDependentValidationResult", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PicamDependentValidationResult)],
            argnames = ["result"] )
    #  ctypes.c_int PicamAdvanced_ValidateDependentParameter(PicamHandle model, ctypes.c_int parameter, ctypes.POINTER(ctypes.POINTER(PicamDependentValidationResult)) result)
    addfunc(lib, "PicamAdvanced_ValidateDependentParameter", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(PicamDependentValidationResult))],
            argnames = ["model", "parameter", "result"] )
    #  ctypes.c_int PicamAdvanced_CommitParametersToCameraDevice(PicamHandle model)
    addfunc(lib, "PicamAdvanced_CommitParametersToCameraDevice", restype = ctypes.c_int,
            argtypes = [PicamHandle],
            argnames = ["model"] )
    #  ctypes.c_int PicamAdvanced_RefreshParameterFromCameraDevice(PicamHandle model, ctypes.c_int parameter)
    addfunc(lib, "PicamAdvanced_RefreshParameterFromCameraDevice", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int],
            argnames = ["model", "parameter"] )
    #  ctypes.c_int PicamAdvanced_RefreshParametersFromCameraDevice(PicamHandle model)
    addfunc(lib, "PicamAdvanced_RefreshParametersFromCameraDevice", restype = ctypes.c_int,
            argtypes = [PicamHandle],
            argnames = ["model"] )
    #  ctypes.c_int PicamAdvanced_GetAcquisitionBuffer(PicamHandle device, ctypes.POINTER(PicamAcquisitionBuffer) buffer)
    addfunc(lib, "PicamAdvanced_GetAcquisitionBuffer", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(PicamAcquisitionBuffer)],
            argnames = ["device", "buffer"] )
    #  ctypes.c_int PicamAdvanced_SetAcquisitionBuffer(PicamHandle device, ctypes.POINTER(PicamAcquisitionBuffer) buffer)
    addfunc(lib, "PicamAdvanced_SetAcquisitionBuffer", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(PicamAcquisitionBuffer)],
            argnames = ["device", "buffer"] )
    #  ctypes.c_int PicamAdvanced_RegisterForAcquisitionUpdated(PicamHandle device, PicamAcquisitionUpdatedCallback updated)
    addfunc(lib, "PicamAdvanced_RegisterForAcquisitionUpdated", restype = ctypes.c_int,
            argtypes = [PicamHandle, PicamAcquisitionUpdatedCallback],
            argnames = ["device", "updated"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForAcquisitionUpdated(PicamHandle device, PicamAcquisitionUpdatedCallback updated)
    addfunc(lib, "PicamAdvanced_UnregisterForAcquisitionUpdated", restype = ctypes.c_int,
            argtypes = [PicamHandle, PicamAcquisitionUpdatedCallback],
            argnames = ["device", "updated"] )
    #  ctypes.c_int PicamAdvanced_CanRegisterForAcquisitionStateUpdated(PicamHandle device, ctypes.c_int state, ctypes.POINTER(pibln) detectable)
    addfunc(lib, "PicamAdvanced_CanRegisterForAcquisitionStateUpdated", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, ctypes.POINTER(pibln)],
            argnames = ["device", "state", "detectable"] )
    #  ctypes.c_int PicamAdvanced_RegisterForAcquisitionStateUpdated(PicamHandle device, ctypes.c_int state, PicamAcquisitionStateUpdatedCallback updated)
    addfunc(lib, "PicamAdvanced_RegisterForAcquisitionStateUpdated", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamAcquisitionStateUpdatedCallback],
            argnames = ["device", "state", "updated"] )
    #  ctypes.c_int PicamAdvanced_UnregisterForAcquisitionStateUpdated(PicamHandle device, ctypes.c_int state, PicamAcquisitionStateUpdatedCallback updated)
    addfunc(lib, "PicamAdvanced_UnregisterForAcquisitionStateUpdated", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.c_int, PicamAcquisitionStateUpdatedCallback],
            argnames = ["device", "state", "updated"] )
    #  ctypes.c_int PicamAdvanced_HasAcquisitionBufferOverrun(PicamHandle device, ctypes.POINTER(pibln) overran)
    addfunc(lib, "PicamAdvanced_HasAcquisitionBufferOverrun", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(pibln)],
            argnames = ["device", "overran"] )
    #  ctypes.c_int PicamAdvanced_CanClearReadoutCountOnline(PicamHandle device, ctypes.POINTER(pibln) clearable)
    addfunc(lib, "PicamAdvanced_CanClearReadoutCountOnline", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(pibln)],
            argnames = ["device", "clearable"] )
    #  ctypes.c_int PicamAdvanced_ClearReadoutCountOnline(PicamHandle device, ctypes.POINTER(pibln) cleared)
    addfunc(lib, "PicamAdvanced_ClearReadoutCountOnline", restype = ctypes.c_int,
            argtypes = [PicamHandle, ctypes.POINTER(pibln)],
            argnames = ["device", "cleared"] )


