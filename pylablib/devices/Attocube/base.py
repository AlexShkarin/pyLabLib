from ...core.devio.comm_backend import DeviceError, DeviceBackendError

class AttocubeError(DeviceError):
    """Generic Attocube error"""
class AttocubeBackendError(AttocubeError,DeviceBackendError):
    """Attocube backend communication error"""