from ...core.devio.comm_backend import DeviceError, DeviceBackendError

class ThorlabsError(DeviceError):
    """Generic Thorlabs error"""
class ThorlabsBackendError(ThorlabsError,DeviceBackendError):
    """Thorlabs backend communication error"""
class ThorlabsTimeoutError(ThorlabsError):
    """Thorlabs timeout error"""