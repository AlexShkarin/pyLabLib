from ...core.devio.comm_backend import DeviceError

class AndorError(DeviceError):
    """Generic Andor error"""
class AndorTimeoutError(AndorError):
    """Andor timeout error"""
class AndorFrameTransferError(AndorError):
    """Andor frame transfer error"""
class AndorNotSupportedError(AndorError):
    """Option not supported error"""