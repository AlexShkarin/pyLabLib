from ...core.devio import comm_backend

class GenericRigolError(comm_backend.DeviceError):
    """Generic Rigol error"""
class GenericRigolBackendError(GenericRigolError,comm_backend.DeviceBackendError):
    """Rigol backend communication error"""