##########   This file is generated automatically based on NIIMAQdx.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class Attributes:
    IMAQdxAttributeBaseAddress                     = ("CameraInformation::BaseAddress")
    IMAQdxAttributeBusType                         = ("CameraInformation::BusType")
    IMAQdxAttributeModelName                       = ("CameraInformation::ModelName")
    IMAQdxAttributeSerialNumberHigh                = ("CameraInformation::SerialNumberHigh")
    IMAQdxAttributeSerialNumberLow                 = ("CameraInformation::SerialNumberLow")
    IMAQdxAttributeVendorName                      = ("CameraInformation::VendorName")
    IMAQdxAttributeHostIPAddress                   = ("CameraInformation::HostIPAddress")
    IMAQdxAttributeIPAddress                       = ("CameraInformation::IPAddress")
    IMAQdxAttributePrimaryURLString                = ("CameraInformation::PrimaryURLString")
    IMAQdxAttributeSecondaryURLString              = ("CameraInformation::SecondaryURLString")
    IMAQdxAttributeAcqInProgress                   = ("StatusInformation::AcqInProgress")
    IMAQdxAttributeLastBufferCount                 = ("StatusInformation::LastBufferCount")
    IMAQdxAttributeLastBufferNumber                = ("StatusInformation::LastBufferNumber")
    IMAQdxAttributeLostBufferCount                 = ("StatusInformation::LostBufferCount")
    IMAQdxAttributeLostPacketCount                 = ("StatusInformation::LostPacketCount")
    IMAQdxAttributeRequestedResendPackets          = ("StatusInformation::RequestedResendPacketCount")
    IMAQdxAttributeReceivedResendPackets           = ("StatusInformation::ReceivedResendPackets")
    IMAQdxAttributeHandledEventCount               = ("StatusInformation::HandledEventCount")
    IMAQdxAttributeLostEventCount                  = ("StatusInformation::LostEventCount")
    IMAQdxAttributeBayerGainB                      = ("AcquisitionAttributes::Bayer::GainB")
    IMAQdxAttributeBayerGainG                      = ("AcquisitionAttributes::Bayer::GainG")
    IMAQdxAttributeBayerGainR                      = ("AcquisitionAttributes::Bayer::GainR")
    IMAQdxAttributeBayerPattern                    = ("AcquisitionAttributes::Bayer::Pattern")
    IMAQdxAttributeStreamChannelMode               = ("AcquisitionAttributes::Controller::StreamChannelMode")
    IMAQdxAttributeDesiredStreamChannel            = ("AcquisitionAttributes::Controller::DesiredStreamChannel")
    IMAQdxAttributeFrameInterval                   = ("AcquisitionAttributes::FrameInterval")
    IMAQdxAttributeIgnoreFirstFrame                = ("AcquisitionAttributes::IgnoreFirstFrame")
    IMAQdxAttributeOffsetX                         = ("OffsetX")
    IMAQdxAttributeOffsetY                         = ("OffsetY")
    IMAQdxAttributeWidth                           = ("Width")
    IMAQdxAttributeHeight                          = ("Height")
    IMAQdxAttributePixelFormat                     = ("PixelFormat")
    IMAQdxAttributePacketSize                      = ("PacketSize")
    IMAQdxAttributePayloadSize                     = ("PayloadSize")
    IMAQdxAttributeSpeed                           = ("AcquisitionAttributes::Speed")
    IMAQdxAttributeShiftPixelBits                  = ("AcquisitionAttributes::ShiftPixelBits")
    IMAQdxAttributeSwapPixelBytes                  = ("AcquisitionAttributes::SwapPixelBytes")
    IMAQdxAttributeOverwriteMode                   = ("AcquisitionAttributes::OverwriteMode")
    IMAQdxAttributeTimeout                         = ("AcquisitionAttributes::Timeout")
    IMAQdxAttributeVideoMode                       = ("AcquisitionAttributes::VideoMode")
    IMAQdxAttributeBitsPerPixel                    = ("AcquisitionAttributes::BitsPerPixel")
    IMAQdxAttributePixelSignedness                 = ("AcquisitionAttributes::PixelSignedness")
    IMAQdxAttributeReserveDualPackets              = ("AcquisitionAttributes::ReserveDualPackets")
    IMAQdxAttributeReceiveTimestampMode            = ("AcquisitionAttributes::ReceiveTimestampMode")
    IMAQdxAttributeActualPeakBandwidth             = ("AcquisitionAttributes::AdvancedEthernet::BandwidthControl::ActualPeakBandwidth")
    IMAQdxAttributeDesiredPeakBandwidth            = ("AcquisitionAttributes::AdvancedEthernet::BandwidthControl::DesiredPeakBandwidth")
    IMAQdxAttributeDestinationMode                 = ("AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMode")
    IMAQdxAttributeDestinationMulticastAddress     = ("AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMulticastAddress")
    IMAQdxAttributeEventsEnabled                   = ("AcquisitionAttributes::AdvancedEthernet::EventParameters::EventsEnabled")
    IMAQdxAttributeMaxOutstandingEvents            = ("AcquisitionAttributes::AdvancedEthernet::EventParameters::MaxOutstandingEvents")
    IMAQdxAttributeTestPacketEnabled               = ("AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::TestPacketEnabled")
    IMAQdxAttributeTestPacketTimeout               = ("AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::TestPacketTimeout")
    IMAQdxAttributeMaxTestPacketRetries            = ("AcquisitionAttributes::AdvancedEthernet::TestPacketParameters::MaxTestPacketRetries")
    IMAQdxAttributeChunkDataDecodingEnabled        = ("AcquisitionAttributes::ChunkDataDecoding::ChunkDataDecodingEnabled")
    IMAQdxAttributeChunkDataDecodingMaxElementSize = ("AcquisitionAttributes::ChunkDataDecoding::MaximumChunkCopySize")
    IMAQdxAttributeLostPacketMode                  = ("AcquisitionAttributes::AdvancedEthernet::LostPacketMode")
    IMAQdxAttributeMemoryWindowSize                = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::MemoryWindowSize")
    IMAQdxAttributeResendsEnabled                  = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendsEnabled")
    IMAQdxAttributeResendThresholdPercentage       = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendThresholdPercentage")
    IMAQdxAttributeResendBatchingPercentage        = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendBatchingPercentage")
    IMAQdxAttributeMaxResendsPerPacket             = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::MaxResendsPerPacket")
    IMAQdxAttributeResendResponseTimeout           = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendResponseTimeout")
    IMAQdxAttributeNewPacketTimeout                = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::NewPacketTimeout")
    IMAQdxAttributeMissingPacketTimeout            = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::MissingPacketTimeout")
    IMAQdxAttributeResendTimerResolution           = ("AcquisitionAttributes::AdvancedEthernet::ResendParameters::ResendTimerResolution")





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
uInt32=ctypes.c_uint
bool32=uInt32
IMAQdxSession=uInt32
class IMAQdxError(enum.IntEnum):
    IMAQdxErrorSuccess                       =_int32(0x0)
    IMAQdxErrorSystemMemoryFull              =_int32(0xBFF69000)
    IMAQdxErrorInternal                      =_int32(0xBFF69001)
    IMAQdxErrorInvalidParameter              =_int32(0xBFF69002)
    IMAQdxErrorInvalidPointer                =_int32(0xBFF69003)
    IMAQdxErrorInvalidInterface              =_int32(0xBFF69004)
    IMAQdxErrorInvalidRegistryKey            =_int32(0xBFF69005)
    IMAQdxErrorInvalidAddress                =_int32(0xBFF69006)
    IMAQdxErrorInvalidDeviceType             =_int32(0xBFF69007)
    IMAQdxErrorNotImplemented                =_int32(0xBFF69008)
    IMAQdxErrorCameraNotFound                =_int32(0xBFF69009)
    IMAQdxErrorCameraInUse                   =_int32(0xBFF6900A)
    IMAQdxErrorCameraNotInitialized          =_int32(0xBFF6900B)
    IMAQdxErrorCameraRemoved                 =_int32(0xBFF6900C)
    IMAQdxErrorCameraRunning                 =_int32(0xBFF6900D)
    IMAQdxErrorCameraNotRunning              =_int32(0xBFF6900E)
    IMAQdxErrorAttributeNotSupported         =_int32(0xBFF6900F)
    IMAQdxErrorAttributeNotSettable          =_int32(0xBFF69010)
    IMAQdxErrorAttributeNotReadable          =_int32(0xBFF69011)
    IMAQdxErrorAttributeOutOfRange           =_int32(0xBFF69012)
    IMAQdxErrorBufferNotAvailable            =_int32(0xBFF69013)
    IMAQdxErrorBufferListEmpty               =_int32(0xBFF69014)
    IMAQdxErrorBufferListLocked              =_int32(0xBFF69015)
    IMAQdxErrorBufferListNotLocked           =_int32(0xBFF69016)
    IMAQdxErrorResourcesAllocated            =_int32(0xBFF69017)
    IMAQdxErrorResourcesUnavailable          =_int32(0xBFF69018)
    IMAQdxErrorAsyncWrite                    =_int32(0xBFF69019)
    IMAQdxErrorAsyncRead                     =_int32(0xBFF6901A)
    IMAQdxErrorTimeout                       =_int32(0xBFF6901B)
    IMAQdxErrorBusReset                      =_int32(0xBFF6901C)
    IMAQdxErrorInvalidXML                    =_int32(0xBFF6901D)
    IMAQdxErrorFileAccess                    =_int32(0xBFF6901E)
    IMAQdxErrorInvalidCameraURLString        =_int32(0xBFF6901F)
    IMAQdxErrorInvalidCameraFile             =_int32(0xBFF69020)
    IMAQdxErrorGenICamError                  =_int32(0xBFF69021)
    IMAQdxErrorFormat7Parameters             =_int32(0xBFF69022)
    IMAQdxErrorInvalidAttributeType          =_int32(0xBFF69023)
    IMAQdxErrorDLLNotFound                   =_int32(0xBFF69024)
    IMAQdxErrorFunctionNotFound              =_int32(0xBFF69025)
    IMAQdxErrorLicenseNotActivated           =_int32(0xBFF69026)
    IMAQdxErrorCameraNotConfiguredForListener=_int32(0xBFF69027)
    IMAQdxErrorCameraMulticastNotAvailable   =_int32(0xBFF69028)
    IMAQdxErrorBufferHasLostPackets          =_int32(0xBFF69029)
    IMAQdxErrorGiGEVisionError               =_int32(0xBFF6902A)
    IMAQdxErrorNetworkError                  =_int32(0xBFF6902B)
    IMAQdxErrorCameraUnreachable             =_int32(0xBFF6902C)
    IMAQdxErrorHighPerformanceNotSupported   =_int32(0xBFF6902D)
    IMAQdxErrorInterfaceNotRenamed           =_int32(0xBFF6902E)
    IMAQdxErrorNoSupportedVideoModes         =_int32(0xBFF6902F)
    IMAQdxErrorSoftwareTriggerOverrun        =_int32(0xBFF69030)
    IMAQdxErrorTestPacketNotReceived         =_int32(0xBFF69031)
    IMAQdxErrorCorruptedImageReceived        =_int32(0xBFF69032)
    IMAQdxErrorCameraConfigurationHasChanged =_int32(0xBFF69033)
    IMAQdxErrorCameraInvalidAuthentication   =_int32(0xBFF69034)
    IMAQdxErrorUnknownHTTPError              =_int32(0xBFF69035)
    IMAQdxErrorKernelDriverUnavailable       =_int32(0xBFF69036)
    IMAQdxErrorPixelFormatDecoderUnavailable =_int32(0xBFF69037)
    IMAQdxErrorFirmwareUpdateNeeded          =_int32(0xBFF69038)
    IMAQdxErrorFirmwareUpdateRebootNeeded    =_int32(0xBFF69039)
    IMAQdxErrorLightingCurrentOutOfRange     =_int32(0xBFF6903A)
    IMAQdxErrorUSB3VisionError               =_int32(0xBFF6903B)
    IMAQdxErrorInvalidU3VUSBDescriptor       =_int32(0xBFF6903C)
    IMAQdxErrorU3VInvalidControlInterface    =_int32(0xBFF6903D)
    IMAQdxErrorU3VControlInterfaceError      =_int32(0xBFF6903E)
    IMAQdxErrorU3VInvalidEventInterface      =_int32(0xBFF6903F)
    IMAQdxErrorU3VEventInterfaceError        =_int32(0xBFF69040)
    IMAQdxErrorU3VInvalidStreamInterface     =_int32(0xBFF69041)
    IMAQdxErrorU3VStreamInterfaceError       =_int32(0xBFF69042)
    IMAQdxErrorU3VUnsupportedConnectionSpeed =_int32(0xBFF69043)
    IMAQdxErrorU3VInsufficientPower          =_int32(0xBFF69044)
    IMAQdxErrorU3VInvalidMaxCurrent          =_int32(0xBFF69045)
    IMAQdxErrorBufferIncompleteData          =_int32(0xBFF69046)
    IMAQdxErrorCameraAcquisitionConfigFailed =_int32(0xBFF69047)
    IMAQdxErrorCameraClosePending            =_int32(0xBFF69048)
    IMAQdxErrorSoftwareFault                 =_int32(0xBFF69049)
    IMAQdxErrorCameraPropertyInvalid         =_int32(0xBFF6904A)
    IMAQdxErrorJumboFramesNotEnabled         =_int32(0xBFF6904B)
    IMAQdxErrorBayerPixelFormatNotSelected   =_int32(0xBFF6904C)
    IMAQdxErrorGuard                         =_int32(0xFFFFFFFF)
dIMAQdxError={a.name:a.value for a in IMAQdxError}
drIMAQdxError={a.value:a.name for a in IMAQdxError}


class IMAQdxBusType(enum.IntEnum):
    IMAQdxBusTypeFireWire  =_int32(0x31333934)
    IMAQdxBusTypeEthernet  =_int32(0x69707634)
    IMAQdxBusTypeSimulator =_int32(0x2073696D)
    IMAQdxBusTypeDirectShow=_int32(0x64736877)
    IMAQdxBusTypeIP        =_int32(0x4950636D)
    IMAQdxBusTypeSmartCam2 =_int32(0x53436132)
    IMAQdxBusTypeUSB3Vision=_int32(0x55534233)
    IMAQdxBusTypeUVC       =_int32(0x55564320)
    IMAQdxBusTypeGuard     =_int32(0xFFFFFFFF)
dIMAQdxBusType={a.name:a.value for a in IMAQdxBusType}
drIMAQdxBusType={a.value:a.name for a in IMAQdxBusType}


class IMAQdxCameraControlMode(enum.IntEnum):
    IMAQdxCameraControlModeController=_int32(0)
    IMAQdxCameraControlModeListener  =_int32(1)
    IMAQdxCameraControlModeGuard     =_int32(0xFFFFFFFF)
dIMAQdxCameraControlMode={a.name:a.value for a in IMAQdxCameraControlMode}
drIMAQdxCameraControlMode={a.value:a.name for a in IMAQdxCameraControlMode}


class IMAQdxBufferNumberMode(enum.IntEnum):
    IMAQdxBufferNumberModeNext        =_int32(0)
    IMAQdxBufferNumberModeLast        =_int32(1)
    IMAQdxBufferNumberModeBufferNumber=_int32(2)
    IMAQdxBufferNumberModeGuard       =_int32(0xFFFFFFFF)
dIMAQdxBufferNumberMode={a.name:a.value for a in IMAQdxBufferNumberMode}
drIMAQdxBufferNumberMode={a.value:a.name for a in IMAQdxBufferNumberMode}


class IMAQdxPnpEvent(enum.IntEnum):
    IMAQdxPnpEventCameraAttached=_int32(0)
    IMAQdxPnpEventCameraDetached=_int32(1)
    IMAQdxPnpEventBusReset      =_int32(2)
    IMAQdxPnpEventGuard         =_int32(0xFFFFFFFF)
dIMAQdxPnpEvent={a.name:a.value for a in IMAQdxPnpEvent}
drIMAQdxPnpEvent={a.value:a.name for a in IMAQdxPnpEvent}


class IMAQdxBayerPattern(enum.IntEnum):
    IMAQdxBayerPatternNone    =_int32(0)
    IMAQdxBayerPatternGB      =_int32(1)
    IMAQdxBayerPatternGR      =_int32(2)
    IMAQdxBayerPatternBG      =_int32(3)
    IMAQdxBayerPatternRG      =_int32(4)
    IMAQdxBayerPatternHardware=_int32(5)
    IMAQdxBayerPatternGuard   =_int32(0xFFFFFFFF)
dIMAQdxBayerPattern={a.name:a.value for a in IMAQdxBayerPattern}
drIMAQdxBayerPattern={a.value:a.name for a in IMAQdxBayerPattern}


class IMAQdxBayerAlgorithm(enum.IntEnum):
    IMAQdxBayerAlgorithmBilinear=_int32(0)
    IMAQdxBayerAlgorithmVNG     =_int32(1)
    IMAQdxBayerAlgorithmGuard   =_int32(0xFFFFFFFF)
dIMAQdxBayerAlgorithm={a.name:a.value for a in IMAQdxBayerAlgorithm}
drIMAQdxBayerAlgorithm={a.value:a.name for a in IMAQdxBayerAlgorithm}


class IMAQdxOutputImageType(enum.IntEnum):
    IMAQdxOutputImageTypeU8   =_int32(0)
    IMAQdxOutputImageTypeI16  =_int32(1)
    IMAQdxOutputImageTypeU16  =_int32(7)
    IMAQdxOutputImageTypeRGB32=_int32(4)
    IMAQdxOutputImageTypeRGB64=_int32(6)
    IMAQdxOutputImageTypeAuto =_int32(0x7FFFFFFF)
    IMAQdxOutputImageTypeGuard=_int32(0xFFFFFFFF)
dIMAQdxOutputImageType={a.name:a.value for a in IMAQdxOutputImageType}
drIMAQdxOutputImageType={a.value:a.name for a in IMAQdxOutputImageType}


class IMAQdxDestinationMode(enum.IntEnum):
    IMAQdxDestinationModeUnicast  =_int32(0)
    IMAQdxDestinationModeBroadcast=_int32(1)
    IMAQdxDestinationModeMulticast=_int32(2)
    IMAQdxDestinationModeGuard    =_int32(0xFFFFFFFF)
dIMAQdxDestinationMode={a.name:a.value for a in IMAQdxDestinationMode}
drIMAQdxDestinationMode={a.value:a.name for a in IMAQdxDestinationMode}


class IMAQdxAttributeType(enum.IntEnum):
    IMAQdxAttributeTypeU32    =_int32(0)
    IMAQdxAttributeTypeI64    =_int32(1)
    IMAQdxAttributeTypeF64    =_int32(2)
    IMAQdxAttributeTypeString =_int32(3)
    IMAQdxAttributeTypeEnum   =_int32(4)
    IMAQdxAttributeTypeBool   =_int32(5)
    IMAQdxAttributeTypeCommand=_int32(6)
    IMAQdxAttributeTypeBlob   =_int32(7)
    IMAQdxAttributeTypeGuard  =_int32(0xFFFFFFFF)
dIMAQdxAttributeType={a.name:a.value for a in IMAQdxAttributeType}
drIMAQdxAttributeType={a.value:a.name for a in IMAQdxAttributeType}


class IMAQdxValueType(enum.IntEnum):
    IMAQdxValueTypeU32             =_int32(0)
    IMAQdxValueTypeI64             =_int32(1)
    IMAQdxValueTypeF64             =_int32(2)
    IMAQdxValueTypeString          =_int32(3)
    IMAQdxValueTypeEnumItem        =_int32(4)
    IMAQdxValueTypeBool            =_int32(5)
    IMAQdxValueTypeDisposableString=_int32(6)
    IMAQdxValueTypeGuard           =_int32(0xFFFFFFFF)
dIMAQdxValueType={a.name:a.value for a in IMAQdxValueType}
drIMAQdxValueType={a.value:a.name for a in IMAQdxValueType}


class IMAQdxInterfaceFileFlags(enum.IntEnum):
    IMAQdxInterfaceFileFlagsConnected=_int32(0x1)
    IMAQdxInterfaceFileFlagsDirty    =_int32(0x2)
    IMAQdxInterfaceFileFlagsGuard    =_int32(0xFFFFFFFF)
dIMAQdxInterfaceFileFlags={a.name:a.value for a in IMAQdxInterfaceFileFlags}
drIMAQdxInterfaceFileFlags={a.value:a.name for a in IMAQdxInterfaceFileFlags}


class IMAQdxOverwriteMode(enum.IntEnum):
    IMAQdxOverwriteModeGetOldest=_int32(0x0)
    IMAQdxOverwriteModeFail     =_int32(0x2)
    IMAQdxOverwriteModeGetNewest=_int32(0x3)
    IMAQdxOverwriteModeGuard    =_int32(0xFFFFFFFF)
dIMAQdxOverwriteMode={a.name:a.value for a in IMAQdxOverwriteMode}
drIMAQdxOverwriteMode={a.value:a.name for a in IMAQdxOverwriteMode}


class IMAQdxIncompleteBufferMode(enum.IntEnum):
    IMAQdxIncompleteBufferModeIgnore=_int32(0)
    IMAQdxIncompleteBufferModeFail  =_int32(1)
    IMAQdxIncompleteBufferModeGuard =_int32(0xFFFFFFFF)
dIMAQdxIncompleteBufferMode={a.name:a.value for a in IMAQdxIncompleteBufferMode}
drIMAQdxIncompleteBufferMode={a.value:a.name for a in IMAQdxIncompleteBufferMode}


class IMAQdxLostPacketMode(enum.IntEnum):
    IMAQdxLostPacketModeIgnore=_int32(0)
    IMAQdxLostPacketModeFail  =_int32(1)
    IMAQdxLostPacketModeGuard =_int32(0xFFFFFFFF)
dIMAQdxLostPacketMode={a.name:a.value for a in IMAQdxLostPacketMode}
drIMAQdxLostPacketMode={a.value:a.name for a in IMAQdxLostPacketMode}


class IMAQdxAttributeVisibility(enum.IntEnum):
    IMAQdxAttributeVisibilitySimple      =_int32(0x00001000)
    IMAQdxAttributeVisibilityIntermediate=_int32(0x00002000)
    IMAQdxAttributeVisibilityAdvanced    =_int32(0x00004000)
    IMAQdxAttributeVisibilityGuard       =_int32(0xFFFFFFFF)
dIMAQdxAttributeVisibility={a.name:a.value for a in IMAQdxAttributeVisibility}
drIMAQdxAttributeVisibility={a.value:a.name for a in IMAQdxAttributeVisibility}


class IMAQdxStreamChannelMode(enum.IntEnum):
    IMAQdxStreamChannelModeAutomatic=_int32(0)
    IMAQdxStreamChannelModeManual   =_int32(1)
    IMAQdxStreamChannelModeGuard    =_int32(0xFFFFFFFF)
dIMAQdxStreamChannelMode={a.name:a.value for a in IMAQdxStreamChannelMode}
drIMAQdxStreamChannelMode={a.value:a.name for a in IMAQdxStreamChannelMode}


class IMAQdxPixelSignedness(enum.IntEnum):
    IMAQdxPixelSignednessUnsigned=_int32(0)
    IMAQdxPixelSignednessSigned  =_int32(1)
    IMAQdxPixelSignednessHardware=_int32(2)
    IMAQdxPixelSignednessGuard   =_int32(0xFFFFFFFF)
dIMAQdxPixelSignedness={a.name:a.value for a in IMAQdxPixelSignedness}
drIMAQdxPixelSignedness={a.value:a.name for a in IMAQdxPixelSignedness}


class IMAQdxUSBConnectionSpeed(enum.IntEnum):
    IMAQdxUSBConnectionSpeedLow  =_int32(1)
    IMAQdxUSBConnectionSpeedFull =_int32(2)
    IMAQdxUSBConnectionSpeedHigh =_int32(4)
    IMAQdxUSBConnectionSpeedSuper=_int32(8)
    IMAQdxUSBConnectionSpeedGuard=_int32(0xFFFFFFFF)
dIMAQdxUSBConnectionSpeed={a.name:a.value for a in IMAQdxUSBConnectionSpeed}
drIMAQdxUSBConnectionSpeed={a.value:a.name for a in IMAQdxUSBConnectionSpeed}


class IMAQdxCameraInformation(ctypes.Structure):
    _fields_=[  ("Type",uInt32),
                ("Version",uInt32),
                ("Flags",uInt32),
                ("SerialNumberHi",uInt32),
                ("SerialNumberLo",uInt32),
                ("BusType",ctypes.c_int),
                ("InterfaceName",ctypes.c_char*512),
                ("VendorName",ctypes.c_char*512),
                ("ModelName",ctypes.c_char*512),
                ("CameraFileName",ctypes.c_char*512),
                ("CameraAttributeURL",ctypes.c_char*512) ]
PIMAQdxCameraInformation=ctypes.POINTER(IMAQdxCameraInformation)
class CIMAQdxCameraInformation(ctypes_wrap.CStructWrapper):
    _struct=IMAQdxCameraInformation


class IMAQdxCameraFile(ctypes.Structure):
    _fields_=[  ("Type",uInt32),
                ("Version",uInt32),
                ("FileName",ctypes.c_char*512) ]
PIMAQdxCameraFile=ctypes.POINTER(IMAQdxCameraFile)
class CIMAQdxCameraFile(ctypes_wrap.CStructWrapper):
    _struct=IMAQdxCameraFile


class IMAQdxAttributeInformation(ctypes.Structure):
    _fields_=[  ("Type",ctypes.c_int),
                ("Readable",bool32),
                ("Writable",bool32),
                ("Name",ctypes.c_char*512) ]
PIMAQdxAttributeInformation=ctypes.POINTER(IMAQdxAttributeInformation)
class CIMAQdxAttributeInformation(ctypes_wrap.CStructWrapper):
    _struct=IMAQdxAttributeInformation


class IMAQdxEnumItem(ctypes.Structure):
    _fields_=[  ("Value",uInt32),
                ("Reserved",uInt32),
                ("Name",ctypes.c_char*512) ]
PIMAQdxEnumItem=ctypes.POINTER(IMAQdxEnumItem)
class CIMAQdxEnumItem(ctypes_wrap.CStructWrapper):
    _struct=IMAQdxEnumItem


IMAQdxVideoMode=IMAQdxEnumItem
FrameDoneEventCallbackPtr=ctypes.c_void_p
PnpEventCallbackPtr=ctypes.c_void_p
AttributeUpdatedEventCallbackPtr=ctypes.c_void_p



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
    #  ctypes.c_int IMAQdxSnap(IMAQdxSession id, ctypes.c_void_p image)
    addfunc(lib, "IMAQdxSnap", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_void_p],
            argnames = ["id", "image"] )
    #  ctypes.c_int IMAQdxConfigureGrab(IMAQdxSession id)
    addfunc(lib, "IMAQdxConfigureGrab", restype = ctypes.c_int,
            argtypes = [IMAQdxSession],
            argnames = ["id"] )
    #  ctypes.c_int IMAQdxGrab(IMAQdxSession id, ctypes.c_void_p image, bool32 waitForNextBuffer, ctypes.POINTER(uInt32) actualBufferNumber)
    addfunc(lib, "IMAQdxGrab", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_void_p, bool32, ctypes.POINTER(uInt32)],
            argnames = ["id", "image", "waitForNextBuffer", "actualBufferNumber"] )
    #  ctypes.c_int IMAQdxSequence(IMAQdxSession id, ctypes.POINTER(ctypes.c_void_p) images, uInt32 count)
    addfunc(lib, "IMAQdxSequence", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.POINTER(ctypes.c_void_p), uInt32],
            argnames = ["id", "images", "count"] )
    #  ctypes.c_int IMAQdxDiscoverEthernetCameras(ctypes.c_char_p address, uInt32 timeout)
    addfunc(lib, "IMAQdxDiscoverEthernetCameras", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, uInt32],
            argnames = ["address", "timeout"] )
    #  ctypes.c_int IMAQdxEnumerateCameras(ctypes.POINTER(IMAQdxCameraInformation) cameraInformationArray, ctypes.POINTER(uInt32) count, bool32 connectedOnly)
    addfunc(lib, "IMAQdxEnumerateCameras", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(IMAQdxCameraInformation), ctypes.POINTER(uInt32), bool32],
            argnames = ["cameraInformationArray", "count", "connectedOnly"] )
    #  ctypes.c_int IMAQdxResetCamera(ctypes.c_char_p name, bool32 resetAll)
    addfunc(lib, "IMAQdxResetCamera", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, bool32],
            argnames = ["name", "resetAll"] )
    #  ctypes.c_int IMAQdxOpenCamera(ctypes.c_char_p name, ctypes.c_int mode, ctypes.POINTER(IMAQdxSession) id)
    addfunc(lib, "IMAQdxOpenCamera", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(IMAQdxSession)],
            argnames = ["name", "mode", "id"] )
    #  ctypes.c_int IMAQdxCloseCamera(IMAQdxSession id)
    addfunc(lib, "IMAQdxCloseCamera", restype = ctypes.c_int,
            argtypes = [IMAQdxSession],
            argnames = ["id"] )
    #  ctypes.c_int IMAQdxConfigureAcquisition(IMAQdxSession id, bool32 continuous, uInt32 bufferCount)
    addfunc(lib, "IMAQdxConfigureAcquisition", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, bool32, uInt32],
            argnames = ["id", "continuous", "bufferCount"] )
    #  ctypes.c_int IMAQdxStartAcquisition(IMAQdxSession id)
    addfunc(lib, "IMAQdxStartAcquisition", restype = ctypes.c_int,
            argtypes = [IMAQdxSession],
            argnames = ["id"] )
    #  ctypes.c_int IMAQdxGetImage(IMAQdxSession id, ctypes.c_void_p image, ctypes.c_int mode, uInt32 desiredBufferNumber, ctypes.POINTER(uInt32) actualBufferNumber)
    addfunc(lib, "IMAQdxGetImage", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_void_p, ctypes.c_int, uInt32, ctypes.POINTER(uInt32)],
            argnames = ["id", "image", "mode", "desiredBufferNumber", "actualBufferNumber"] )
    #  ctypes.c_int IMAQdxGetImageData(IMAQdxSession id, ctypes.c_void_p buffer, uInt32 bufferSize, ctypes.c_int mode, uInt32 desiredBufferNumber, ctypes.POINTER(uInt32) actualBufferNumber)
    addfunc(lib, "IMAQdxGetImageData", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_void_p, uInt32, ctypes.c_int, uInt32, ctypes.POINTER(uInt32)],
            argnames = ["id", "buffer", "bufferSize", "mode", "desiredBufferNumber", "actualBufferNumber"] )
    #  ctypes.c_int IMAQdxStopAcquisition(IMAQdxSession id)
    addfunc(lib, "IMAQdxStopAcquisition", restype = ctypes.c_int,
            argtypes = [IMAQdxSession],
            argnames = ["id"] )
    #  ctypes.c_int IMAQdxUnconfigureAcquisition(IMAQdxSession id)
    addfunc(lib, "IMAQdxUnconfigureAcquisition", restype = ctypes.c_int,
            argtypes = [IMAQdxSession],
            argnames = ["id"] )
    #  ctypes.c_int IMAQdxEnumerateVideoModes(IMAQdxSession id, ctypes.POINTER(IMAQdxVideoMode) videoModeArray, ctypes.POINTER(uInt32) count, ctypes.POINTER(uInt32) currentMode)
    addfunc(lib, "IMAQdxEnumerateVideoModes", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.POINTER(IMAQdxVideoMode), ctypes.POINTER(uInt32), ctypes.POINTER(uInt32)],
            argnames = ["id", "videoModeArray", "count", "currentMode"] )
    #  ctypes.c_int IMAQdxEnumerateAttributes(IMAQdxSession id, ctypes.POINTER(IMAQdxAttributeInformation) attributeInformationArray, ctypes.POINTER(uInt32) count, ctypes.c_char_p root)
    addfunc(lib, "IMAQdxEnumerateAttributes", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.POINTER(IMAQdxAttributeInformation), ctypes.POINTER(uInt32), ctypes.c_char_p],
            argnames = ["id", "attributeInformationArray", "count", "root"] )
    #  ctypes.c_int IMAQdxGetAttribute(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ctypes.c_void_p value)
    addfunc(lib, "IMAQdxGetAttribute", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p],
            argnames = ["id", "name", "type", "value"] )
    #  ctypes.c_int IMAQdxSetAttribute(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ...)
    addfunc(lib, "IMAQdxSetAttribute", restype = ctypes.c_int,
            argtypes = None,
            argnames = None )
    #  ctypes.c_int IMAQdxGetAttributeMinimum(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ctypes.c_void_p value)
    addfunc(lib, "IMAQdxGetAttributeMinimum", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p],
            argnames = ["id", "name", "type", "value"] )
    #  ctypes.c_int IMAQdxGetAttributeMaximum(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ctypes.c_void_p value)
    addfunc(lib, "IMAQdxGetAttributeMaximum", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p],
            argnames = ["id", "name", "type", "value"] )
    #  ctypes.c_int IMAQdxGetAttributeIncrement(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_int type, ctypes.c_void_p value)
    addfunc(lib, "IMAQdxGetAttributeIncrement", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p],
            argnames = ["id", "name", "type", "value"] )
    #  ctypes.c_int IMAQdxGetAttributeType(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int) type)
    addfunc(lib, "IMAQdxGetAttributeType", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["id", "name", "type"] )
    #  ctypes.c_int IMAQdxIsAttributeReadable(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(bool32) readable)
    addfunc(lib, "IMAQdxIsAttributeReadable", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.POINTER(bool32)],
            argnames = ["id", "name", "readable"] )
    #  ctypes.c_int IMAQdxIsAttributeWritable(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(bool32) writable)
    addfunc(lib, "IMAQdxIsAttributeWritable", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.POINTER(bool32)],
            argnames = ["id", "name", "writable"] )
    #  ctypes.c_int IMAQdxEnumerateAttributeValues(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(IMAQdxEnumItem) list, ctypes.POINTER(uInt32) size)
    addfunc(lib, "IMAQdxEnumerateAttributeValues", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.POINTER(IMAQdxEnumItem), ctypes.POINTER(uInt32)],
            argnames = ["id", "name", "list", "size"] )
    #  ctypes.c_int IMAQdxGetAttributeTooltip(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_char_p tooltip, uInt32 length)
    addfunc(lib, "IMAQdxGetAttributeTooltip", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.c_char_p, uInt32],
            argnames = ["id", "name", "tooltip", "length"] )
    #  ctypes.c_int IMAQdxGetAttributeUnits(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_char_p units, uInt32 length)
    addfunc(lib, "IMAQdxGetAttributeUnits", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.c_char_p, uInt32],
            argnames = ["id", "name", "units", "length"] )
    #  ctypes.c_int IMAQdxRegisterFrameDoneEvent(IMAQdxSession id, uInt32 bufferInterval, FrameDoneEventCallbackPtr callbackFunction, ctypes.c_void_p callbackData)
    addfunc(lib, "IMAQdxRegisterFrameDoneEvent", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, uInt32, FrameDoneEventCallbackPtr, ctypes.c_void_p],
            argnames = ["id", "bufferInterval", "callbackFunction", "callbackData"] )
    #  ctypes.c_int IMAQdxRegisterPnpEvent(IMAQdxSession id, ctypes.c_int event, PnpEventCallbackPtr callbackFunction, ctypes.c_void_p callbackData)
    addfunc(lib, "IMAQdxRegisterPnpEvent", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_int, PnpEventCallbackPtr, ctypes.c_void_p],
            argnames = ["id", "event", "callbackFunction", "callbackData"] )
    #  ctypes.c_int IMAQdxWriteRegister(IMAQdxSession id, uInt32 offset, uInt32 value)
    addfunc(lib, "IMAQdxWriteRegister", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, uInt32, uInt32],
            argnames = ["id", "offset", "value"] )
    #  ctypes.c_int IMAQdxReadRegister(IMAQdxSession id, uInt32 offset, ctypes.POINTER(uInt32) value)
    addfunc(lib, "IMAQdxReadRegister", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, uInt32, ctypes.POINTER(uInt32)],
            argnames = ["id", "offset", "value"] )
    #  ctypes.c_int IMAQdxWriteMemory(IMAQdxSession id, uInt32 offset, ctypes.c_char_p values, uInt32 count)
    addfunc(lib, "IMAQdxWriteMemory", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, uInt32, ctypes.c_char_p, uInt32],
            argnames = ["id", "offset", "values", "count"] )
    #  ctypes.c_int IMAQdxReadMemory(IMAQdxSession id, uInt32 offset, ctypes.c_char_p values, uInt32 count)
    addfunc(lib, "IMAQdxReadMemory", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, uInt32, ctypes.c_char_p, uInt32],
            argnames = ["id", "offset", "values", "count"] )
    #  ctypes.c_int IMAQdxGetErrorString(ctypes.c_int error, ctypes.c_char_p message, uInt32 messageLength)
    addfunc(lib, "IMAQdxGetErrorString", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_char_p, uInt32],
            argnames = ["error", "message", "messageLength"] )
    #  ctypes.c_int IMAQdxWriteAttributes(IMAQdxSession id, ctypes.c_char_p filename)
    addfunc(lib, "IMAQdxWriteAttributes", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p],
            argnames = ["id", "filename"] )
    #  ctypes.c_int IMAQdxReadAttributes(IMAQdxSession id, ctypes.c_char_p filename)
    addfunc(lib, "IMAQdxReadAttributes", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p],
            argnames = ["id", "filename"] )
    #  ctypes.c_int IMAQdxResetEthernetCameraAddress(ctypes.c_char_p name, ctypes.c_char_p address, ctypes.c_char_p subnet, ctypes.c_char_p gateway, uInt32 timeout)
    addfunc(lib, "IMAQdxResetEthernetCameraAddress", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, uInt32],
            argnames = ["name", "address", "subnet", "gateway", "timeout"] )
    #  ctypes.c_int IMAQdxEnumerateAttributes2(IMAQdxSession id, ctypes.POINTER(IMAQdxAttributeInformation) attributeInformationArray, ctypes.POINTER(uInt32) count, ctypes.c_char_p root, ctypes.c_int visibility)
    addfunc(lib, "IMAQdxEnumerateAttributes2", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.POINTER(IMAQdxAttributeInformation), ctypes.POINTER(uInt32), ctypes.c_char_p, ctypes.c_int],
            argnames = ["id", "attributeInformationArray", "count", "root", "visibility"] )
    #  ctypes.c_int IMAQdxGetAttributeVisibility(IMAQdxSession id, ctypes.c_char_p name, ctypes.POINTER(ctypes.c_int) visibility)
    addfunc(lib, "IMAQdxGetAttributeVisibility", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["id", "name", "visibility"] )
    #  ctypes.c_int IMAQdxGetAttributeDescription(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_char_p description, uInt32 length)
    addfunc(lib, "IMAQdxGetAttributeDescription", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.c_char_p, uInt32],
            argnames = ["id", "name", "description", "length"] )
    #  ctypes.c_int IMAQdxGetAttributeDisplayName(IMAQdxSession id, ctypes.c_char_p name, ctypes.c_char_p displayName, uInt32 length)
    addfunc(lib, "IMAQdxGetAttributeDisplayName", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, ctypes.c_char_p, uInt32],
            argnames = ["id", "name", "displayName", "length"] )
    #  ctypes.c_int IMAQdxDispose(ctypes.c_void_p buffer)
    addfunc(lib, "IMAQdxDispose", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["buffer"] )
    #  ctypes.c_int IMAQdxRegisterAttributeUpdatedEvent(IMAQdxSession id, ctypes.c_char_p name, AttributeUpdatedEventCallbackPtr callbackFunction, ctypes.c_void_p callbackData)
    addfunc(lib, "IMAQdxRegisterAttributeUpdatedEvent", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.c_char_p, AttributeUpdatedEventCallbackPtr, ctypes.c_void_p],
            argnames = ["id", "name", "callbackFunction", "callbackData"] )
    #  ctypes.c_int IMAQdxEnumerateAttributes3(IMAQdxSession id, ctypes.POINTER(IMAQdxAttributeInformation) attributeInformationArray, ctypes.POINTER(uInt32) count, ctypes.c_char_p root, ctypes.c_int visibility)
    addfunc(lib, "IMAQdxEnumerateAttributes3", restype = ctypes.c_int,
            argtypes = [IMAQdxSession, ctypes.POINTER(IMAQdxAttributeInformation), ctypes.POINTER(uInt32), ctypes.c_char_p, ctypes.c_int],
            argnames = ["id", "attributeInformationArray", "count", "root", "visibility"] )


