from ...core.devio import comm_backend

class GenericSirahError(comm_backend.DeviceError):
    """Generic Sirah error"""
class GenericSirahBackendError(GenericSirahError,comm_backend.DeviceBackendError):
    """Sirah backend communication error"""