"""
Dealing with Python2 / Python3 compatibility.
"""
from builtins import bytes as new_bytes

if str is bytes: # Python 2

    textstring=(basestring,)  # pylint: disable=undefined-variable
    bytestring=(str,new_bytes)
    anystring=(str,unicode)  # pylint: disable=undefined-variable

    def as_str(data):
        """Convert a string into a text string"""
        return data
    def as_bytes(data):
        """Convert a string into bytes"""
        return new_bytes(data)
    def as_builtin_bytes(data):
        """Convert a string into builtin bytes (str in Python 2, bytes in Python 3)"""
        return data

else:

    import locale
    locenc=locale.getpreferredencoding()
    use_locenc=True

    textstring=(str,)
    bytestring=(bytes,)
    anystring=(str,bytes)

    def as_str(data):
        """Convert a string into a text string"""
        try:
            return data if isinstance(data,str) else data.decode()
        except UnicodeDecodeError:
            if use_locenc:
                return data.decode(encoding=locenc)
            raise
    def as_bytes(data):
        """Convert a string into bytes"""
        return data if isinstance(data,bytes) else (data.encode("utf-8") if isinstance(data,str) else bytes(data))
    as_builtin_bytes=as_bytes

def as_datatype(data, datatype):
    """
    Convert a string into a given datatypes.

    `datatype` can be ``"str"`` (text string), ``"bytes"`` (byte string), or ``"auto"`` (no conversion).
    """
    if datatype=="auto":
        return data
    elif datatype=="str":
        return as_str(data)
    return as_bytes(data)