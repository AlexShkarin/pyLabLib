_tables={}


def binv(a, l):
    """Reverse bit order of `a` treating it as an `l`-bit number"""
    ai=0
    for _ in range(l):
        ai=(ai<<1)|(a&0x01)
        a>>=1
    return ai
_bi=[binv(i,8) for i in range(0x100)]


def _get_polylen(poly):
    if poly<0x100:
        return 1
    if poly<0x10000:
        return 2
    if poly<0x100000000:
        return 4
    raise ValueError("polynomial {} is too long")
    
def calc_table(poly, ref=False):
    """
    Calculate CRC byte table for the given polynomial and reflection parameter.

    `ref` specifies whether both input and output bit sequences are reflected.
    """
    table=[]
    l=_get_polylen(poly)
    msb=1<<(l*8-1)
    mask=(1<<l*8)-1
    for i in range(0x100):
        if ref:
            i=_bi[i]
        for _ in range(l*8):
            d=i&msb
            i=(i<<1)&mask
            if d:
                i^=poly
        if ref:
            i=binv(i,l*8)
        table.append(i)
    return table

def crc(msg, poly, refin=False, refout=False, init=0, xorout=0):
    """
    Calculate CRC for the given message, polynomial, and additional parameters.

    `msg` should be a bytes object, while `poly` is an integer with the polynomial coefficients.
    """
    tk=(poly,refin)
    if tk not in _tables:
        _tables[tk]=calc_table(poly,ref=refin)
    t=_tables[tk]
    l=_get_polylen(poly)
    msboff=(l-1)*8
    mask=(1<<l*8)-1
    v=init
    if not refin:
        for b in msg:
            p=((v>>msboff)&0xFF)^b
            v=((v<<8)&mask)^t[p]
    else:
        for b in msg:
            p=(v&0xFF)^b
            v=((v>>8)&mask)^t[p]
    if refout!=refin:
        v=binv(v,l*8)
    return v^xorout