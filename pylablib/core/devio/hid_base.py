##### Errors declaration #####

class HIDError(RuntimeError):
    """Generic HID error"""
class HIDLibError(HIDError):
    """Generic HID library boolean function error"""
    def __init__(self, func, code):
        self.func=func
        self.code=code
        msg="function {} returned FALSE; last error code is {}(0x{:08X})".format(func,code,code%0x100000000)
        super().__init__(msg)
class HIDTimeoutError(HIDError):
    """HID read timeout error"""