from ...core.devio import comm_backend

class AgilentError(comm_backend.DeviceError):
    """Generic Agilent device error"""
class AgilentBackendError(AgilentError,comm_backend.DeviceBackendError):
    """Generic Agilent backend communication error"""
