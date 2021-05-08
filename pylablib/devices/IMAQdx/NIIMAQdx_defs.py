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
    IMAQdxErrorInternal                      =enum.auto()
    IMAQdxErrorInvalidParameter              =enum.auto()
    IMAQdxErrorInvalidPointer                =enum.auto()
    IMAQdxErrorInvalidInterface              =enum.auto()
    IMAQdxErrorInvalidRegistryKey            =enum.auto()
    IMAQdxErrorInvalidAddress                =enum.auto()
    IMAQdxErrorInvalidDeviceType             =enum.auto()
    IMAQdxErrorNotImplemented                =enum.auto()
    IMAQdxErrorCameraNotFound                =enum.auto()
    IMAQdxErrorCameraInUse                   =enum.auto()
    IMAQdxErrorCameraNotInitialized          =enum.auto()
    IMAQdxErrorCameraRemoved                 =enum.auto()
    IMAQdxErrorCameraRunning                 =enum.auto()
    IMAQdxErrorCameraNotRunning              =enum.auto()
    IMAQdxErrorAttributeNotSupported         =enum.auto()
    IMAQdxErrorAttributeNotSettable          =enum.auto()
    IMAQdxErrorAttributeNotReadable          =enum.auto()
    IMAQdxErrorAttributeOutOfRange           =enum.auto()
    IMAQdxErrorBufferNotAvailable            =enum.auto()
    IMAQdxErrorBufferListEmpty               =enum.auto()
    IMAQdxErrorBufferListLocked              =enum.auto()
    IMAQdxErrorBufferListNotLocked           =enum.auto()
    IMAQdxErrorResourcesAllocated            =enum.auto()
    IMAQdxErrorResourcesUnavailable          =enum.auto()
    IMAQdxErrorAsyncWrite                    =enum.auto()
    IMAQdxErrorAsyncRead                     =enum.auto()
    IMAQdxErrorTimeout                       =enum.auto()
    IMAQdxErrorBusReset                      =enum.auto()
    IMAQdxErrorInvalidXML                    =enum.auto()
    IMAQdxErrorFileAccess                    =enum.auto()
    IMAQdxErrorInvalidCameraURLString        =enum.auto()
    IMAQdxErrorInvalidCameraFile             =enum.auto()
    IMAQdxErrorGenICamError                  =enum.auto()
    IMAQdxErrorFormat7Parameters             =enum.auto()
    IMAQdxErrorInvalidAttributeType          =enum.auto()
    IMAQdxErrorDLLNotFound                   =enum.auto()
    IMAQdxErrorFunctionNotFound              =enum.auto()
    IMAQdxErrorLicenseNotActivated           =enum.auto()
    IMAQdxErrorCameraNotConfiguredForListener=enum.auto()
    IMAQdxErrorCameraMulticastNotAvailable   =enum.auto()
    IMAQdxErrorBufferHasLostPackets          =enum.auto()
    IMAQdxErrorGiGEVisionError               =enum.auto()
    IMAQdxErrorNetworkError                  =enum.auto()
    IMAQdxErrorCameraUnreachable             =enum.auto()
    IMAQdxErrorHighPerformanceNotSupported   =enum.auto()
    IMAQdxErrorInterfaceNotRenamed           =enum.auto()
    IMAQdxErrorNoSupportedVideoModes         =enum.auto()
    IMAQdxErrorSoftwareTriggerOverrun        =enum.auto()
    IMAQdxErrorTestPacketNotReceived         =enum.auto()
    IMAQdxErrorCorruptedImageReceived        =enum.auto()
    IMAQdxErrorCameraConfigurationHasChanged =enum.auto()
    IMAQdxErrorCameraInvalidAuthentication   =enum.auto()
    IMAQdxErrorUnknownHTTPError              =enum.auto()
    IMAQdxErrorKernelDriverUnavailable       =enum.auto()
    IMAQdxErrorPixelFormatDecoderUnavailable =enum.auto()
    IMAQdxErrorFirmwareUpdateNeeded          =enum.auto()
    IMAQdxErrorFirmwareUpdateRebootNeeded    =enum.auto()
    IMAQdxErrorLightingCurrentOutOfRange     =enum.auto()
    IMAQdxErrorUSB3VisionError               =enum.auto()
    IMAQdxErrorInvalidU3VUSBDescriptor       =enum.auto()
    IMAQdxErrorU3VInvalidControlInterface    =enum.auto()
    IMAQdxErrorU3VControlInterfaceError      =enum.auto()
    IMAQdxErrorU3VInvalidEventInterface      =enum.auto()
    IMAQdxErrorU3VEventInterfaceError        =enum.auto()
    IMAQdxErrorU3VInvalidStreamInterface     =enum.auto()
    IMAQdxErrorU3VStreamInterfaceError       =enum.auto()
    IMAQdxErrorU3VUnsupportedConnectionSpeed =enum.auto()
    IMAQdxErrorU3VInsufficientPower          =enum.auto()
    IMAQdxErrorU3VInvalidMaxCurrent          =enum.auto()
    IMAQdxErrorBufferIncompleteData          =enum.auto()
    IMAQdxErrorCameraAcquisitionConfigFailed =enum.auto()
    IMAQdxErrorCameraClosePending            =enum.auto()
    IMAQdxErrorSoftwareFault                 =enum.auto()
    IMAQdxErrorCameraPropertyInvalid         =enum.auto()
    IMAQdxErrorJumboFramesNotEnabled         =enum.auto()
    IMAQdxErrorBayerPixelFormatNotSelected   =enum.auto()
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
    IMAQdxCameraControlModeListener  =enum.auto()
    IMAQdxCameraControlModeGuard     =_int32(0xFFFFFFFF)
dIMAQdxCameraControlMode={a.name:a.value for a in IMAQdxCameraControlMode}
drIMAQdxCameraControlMode={a.value:a.name for a in IMAQdxCameraControlMode}


class IMAQdxBufferNumberMode(enum.IntEnum):
    IMAQdxBufferNumberModeNext        =_int32(0)
    IMAQdxBufferNumberModeLast        =enum.auto()
    IMAQdxBufferNumberModeBufferNumber=enum.auto()
    IMAQdxBufferNumberModeGuard       =_int32(0xFFFFFFFF)
dIMAQdxBufferNumberMode={a.name:a.value for a in IMAQdxBufferNumberMode}
drIMAQdxBufferNumberMode={a.value:a.name for a in IMAQdxBufferNumberMode}


class IMAQdxPnpEvent(enum.IntEnum):
    IMAQdxPnpEventCameraAttached=_int32(0)
    IMAQdxPnpEventCameraDetached=enum.auto()
    IMAQdxPnpEventBusReset      =enum.auto()
    IMAQdxPnpEventGuard         =_int32(0xFFFFFFFF)
dIMAQdxPnpEvent={a.name:a.value for a in IMAQdxPnpEvent}
drIMAQdxPnpEvent={a.value:a.name for a in IMAQdxPnpEvent}


class IMAQdxBayerPattern(enum.IntEnum):
    IMAQdxBayerPatternNone    =_int32(0)
    IMAQdxBayerPatternGB      =enum.auto()
    IMAQdxBayerPatternGR      =enum.auto()
    IMAQdxBayerPatternBG      =enum.auto()
    IMAQdxBayerPatternRG      =enum.auto()
    IMAQdxBayerPatternHardware=enum.auto()
    IMAQdxBayerPatternGuard   =_int32(0xFFFFFFFF)
dIMAQdxBayerPattern={a.name:a.value for a in IMAQdxBayerPattern}
drIMAQdxBayerPattern={a.value:a.name for a in IMAQdxBayerPattern}


class IMAQdxBayerAlgorithm(enum.IntEnum):
    IMAQdxBayerAlgorithmBilinear=_int32(0)
    IMAQdxBayerAlgorithmVNG     =enum.auto()
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
    IMAQdxDestinationModeBroadcast=enum.auto()
    IMAQdxDestinationModeMulticast=enum.auto()
    IMAQdxDestinationModeGuard    =_int32(0xFFFFFFFF)
dIMAQdxDestinationMode={a.name:a.value for a in IMAQdxDestinationMode}
drIMAQdxDestinationMode={a.value:a.name for a in IMAQdxDestinationMode}


class IMAQdxAttributeType(enum.IntEnum):
    IMAQdxAttributeTypeU32    =_int32(0)
    IMAQdxAttributeTypeI64    =enum.auto()
    IMAQdxAttributeTypeF64    =enum.auto()
    IMAQdxAttributeTypeString =enum.auto()
    IMAQdxAttributeTypeEnum   =enum.auto()
    IMAQdxAttributeTypeBool   =enum.auto()
    IMAQdxAttributeTypeCommand=enum.auto()
    IMAQdxAttributeTypeBlob   =enum.auto()
    IMAQdxAttributeTypeGuard  =_int32(0xFFFFFFFF)
dIMAQdxAttributeType={a.name:a.value for a in IMAQdxAttributeType}
drIMAQdxAttributeType={a.value:a.name for a in IMAQdxAttributeType}


class IMAQdxValueType(enum.IntEnum):
    IMAQdxValueTypeU32             =_int32(0)
    IMAQdxValueTypeI64             =enum.auto()
    IMAQdxValueTypeF64             =enum.auto()
    IMAQdxValueTypeString          =enum.auto()
    IMAQdxValueTypeEnumItem        =enum.auto()
    IMAQdxValueTypeBool            =enum.auto()
    IMAQdxValueTypeDisposableString=enum.auto()
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
    IMAQdxIncompleteBufferModeFail  =enum.auto()
    IMAQdxIncompleteBufferModeGuard =_int32(0xFFFFFFFF)
dIMAQdxIncompleteBufferMode={a.name:a.value for a in IMAQdxIncompleteBufferMode}
drIMAQdxIncompleteBufferMode={a.value:a.name for a in IMAQdxIncompleteBufferMode}


class IMAQdxLostPacketMode(enum.IntEnum):
    IMAQdxLostPacketModeIgnore=_int32(0)
    IMAQdxLostPacketModeFail  =enum.auto()
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
    IMAQdxStreamChannelModeManual   =enum.auto()
    IMAQdxStreamChannelModeGuard    =_int32(0xFFFFFFFF)
dIMAQdxStreamChannelMode={a.name:a.value for a in IMAQdxStreamChannelMode}
drIMAQdxStreamChannelMode={a.value:a.name for a in IMAQdxStreamChannelMode}


class IMAQdxPixelSignedness(enum.IntEnum):
    IMAQdxPixelSignednessUnsigned=_int32(0)
    IMAQdxPixelSignednessSigned  =enum.auto()
    IMAQdxPixelSignednessHardware=enum.auto()
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


