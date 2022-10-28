from ...core.devio.comm_backend import DeviceError

class MightexError(DeviceError):
    """Generic Mightex error"""
class MightexTimeoutError(MightexError):
    "Mightex frame timeout error"