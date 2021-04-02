class AndorError(RuntimeError):
    """Generic Andor error"""
class AndorTimeoutError(AndorError):
    """Andor timeout error"""
class AndorNotSupportedError(AndorError):
    """Option not supported error"""