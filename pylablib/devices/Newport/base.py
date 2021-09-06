from ...core.devio.comm_backend import DeviceError, DeviceBackendError

class NewportError(DeviceError):
    """Generic Newport device error"""
class NewportBackendError(NewportError,DeviceBackendError):
    """Newport backend communication error"""