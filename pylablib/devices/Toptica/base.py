from ...core.devio.comm_backend import DeviceError, DeviceBackendError

class TopticaError(DeviceError):
    """Generic Toptica device error"""
class TopticaBackendError(TopticaError,DeviceBackendError):
    """Toptica backend communication error"""