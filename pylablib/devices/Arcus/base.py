from ...core.devio.comm_backend import DeviceError, DeviceBackendError

class ArcusError(DeviceError):
    """Generic Arcus error"""
class ArcusBackendError(ArcusError,DeviceBackendError):
    """Generic Arcus backend communication error"""