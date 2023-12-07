from ...core.devio import comm_backend

class HubnerError(comm_backend.DeviceError):
    """Generic Hubner Photonics devices error"""
class HubnerBackendError(HubnerError,comm_backend.DeviceBackendError):
    """Generic Hubner Photonics backend communication error"""

