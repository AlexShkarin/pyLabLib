from ...core.devio import comm_backend

class GenericKeithleyError(comm_backend.DeviceError):
    """Generic Keithley error"""
class GenericKeithleyBackendError(GenericKeithleyError,comm_backend.DeviceBackendError):
    """Keithley backend communication error"""