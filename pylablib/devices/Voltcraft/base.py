from ...core.devio import comm_backend

class GenericVoltcraftError(comm_backend.DeviceError):
    """Generic Voltcraft error"""
class GenericVoltcraftBackendError(GenericVoltcraftError,comm_backend.DeviceBackendError):
    """Voltcraft backend communication error"""