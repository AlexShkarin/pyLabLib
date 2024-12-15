class ITransformer:
    """Generic binary data transformer"""
    def f2d(self, fbytes):
        """Transform stored file bytes into data bytes"""
        return fbytes
    def d2f(self, dbytes):
        """Transform data bytes into stored file bytes"""
        return dbytes


class MaskTransformer:
    """XOR mask transformer"""
    def __init__(self, mask):
        self.mask=mask.encode() if isinstance(mask,str) else bytes(mask)
    def f2d(self, fbytes):
        if not fbytes:
            return fbytes
        mrep=(len(fbytes)-1)//len(self.mask)+1
        rmask=(self.mask*mrep)[:len(fbytes)]
        return bytes([cm^cb for cm,cb in zip(rmask,fbytes)])
    def d2f(self, dbytes):
        return self.f2d(dbytes)