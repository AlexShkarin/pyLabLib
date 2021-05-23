"""Binary files input/output"""


from ..utils import general, py3
import numpy as np
import pickle
import contextlib



##### Complex structures file IO #####

default_byteorder="<"
_sbase=0x01
_tbase=0x10
_bobase=0x20

fdtypes={0x40:">f2",0x41:">f4",0x42:">f8",0x60:"<f2",0x61:"<f4",0x62:"<f8"}
fdtypes_inv=general.invert_dict(fdtypes)
idtypes={0x00:"<i1",0x01:"<i2",0x02:"<i4",0x03:"<i8",0x10:"<u1",0x11:"<u2",0x12:"<u4",0x13:"<u8",
        0x20:">i1",0x21:">i2",0x22:">i4",0x23:">i8",0x30:">u1",0x31:">u2",0x32:">u4",0x33:">u8"}
idtypes_inv=general.invert_dict(idtypes)
sdtypes={0x80:"sp<u1",0x81:"sp<u2",0x82:"sp<u4",0x83:"sp<u8",
         0xa0:"sp>u1",0xa1:"sp>u2",0xa2:"sp>u4",0xa3:"sp>u8"}
sdtypes_inv=general.invert_dict(sdtypes)
pkdtypes={}
for pkp in [0,1,2,3]:
    for bo in [0,1]:
        for s in [1,2,4,8]:
            pkdtypes[0x100+0x40*pkp+0x20*bo+s]="pk{}{}u{}".format(pkp,"<>"[bo],s)
pkdtypes_inv=general.invert_dict(pkdtypes)
asdtypes={0x1000:"as<u1",0x1001:"as<u2",0x1020:"as>u1",0x1021:"as>u2"}
asdtypes_inv=general.invert_dict(asdtypes)

alltypes=general.merge_dicts(fdtypes,idtypes,sdtypes,pkdtypes)
alltypes_inv=general.invert_dict(alltypes)

def write_num(x, f, dtype):
    """
    Write a number `x` into file `f`.

    `dtype` is the textual representation of data type (numpy-style).
    """
    if dtype[0] not in "<>":
        dtype=default_byteorder+dtype
    if dtype in idtypes_inv:
        np.asarray(int(x)).astype(dtype).tofile(f)
    elif dtype in fdtypes_inv:
        np.asarray(float(x)).astype(dtype).tofile(f)
    else:
        raise ValueError("unrecognized dtype: {}".format(dtype))
def write_str(s, f, dtype, strict=False):
    """
    Write a string `s` into a file `f`.

    `dtype` is the textual representation of data type. Can be ``"s"`` (simply translate into bytes and write),
    ``"sp"+sdtype`` (e.g., ``"sp<u2"``), where the string is prepended by its length written using ``sdtype`` format,
    or ``"s"+len`` (e.g., ``"s16"``), where ``len`` is the textual representation of string length (written data is equivalent to ``"s"`` format).

    If ``strict==True``, raise error if string length is incompatible with the format
    (too long for a given ``"sp"``-type prefix, or doesn't agree with ``"s"``-type length).
    """
    s=py3.as_bytes(s)
    if dtype=="s":
        f.write(s)
    elif dtype.startswith("sp"):
        iinfo=np.iinfo(dtype[2:])
        if strict and len(s)>iinfo.max:
            raise ValueError("string length {} doesn't agree with length dtype {}".format(len(s),dtype[2:]))
        slen=min(iinfo.max,len(s))
        write_num(slen,f,dtype[2:])
        f.write(s[:slen])
    elif dtype.startswith("s"):
        if strict and len(s)!=int(dtype[1:]):
            raise ValueError("string length {} doesn't agree with dtype {}".format(len(s),int(dtype[1:])))
        f.write(s)
    else:
        raise ValueError("unrecognized dtype: {}".format(dtype))
def write_pickle(v, f, dtype):
    """
    Write a value `v` into file `f` as a Python pickle object.

    `dtype` is the textual representation of data type (numpy-style), and should be ``"pk"+proto+sdtype`` (e.g., ``"pk3<u2"``),
    where ``proto`` is the textual representation of the pickle protocol,
    and ``sdtype`` is the data type of the prepended string length (see ``"sp"+sdtype`` type in :func:`write_str`).
    """
    if dtype.startswith("pk"):
        proto=int(dtype[2])
        sdtype=dtype[3:]
        v=pickle.dumps(v,protocol=proto)
        write_str(v,f,"sp"+sdtype)
    else:
        raise ValueError("unrecognized dtype: {}".format(dtype))
def write_val(v, f, dtype):
    """
    Write an arbitrary value `v` into file `f` using the supplied `dtype`.

    Storage type depends on `dtype`: can be string (see :func:`write_str`), number (see :func:`write_num`), or pickled value (see :func:`write_pickle`).
    In addition, `dtype` can be a tuple of dtypes with length equal to the length of `v`, in which case the values in `v` are written sequentially.
    """
    if isinstance(dtype,py3.textstring):
        if dtype.startswith("s"):
            write_str(v,f,dtype)
        elif dtype.startswith("pk"):
            write_pickle(v,f,dtype)
        else:
            write_num(v,f,dtype)
    if isinstance(dtype,tuple):
        if len(v)!=len(dtype):
            raise ValueError("value {} doesn't agree with dtype {}".format(v,dtype))
        for (el,dt) in zip(v,dtype):
            write_val(el,f,dt)

def read_num(f, dtype):
    """
    Read a number from file `f`.

    `dtype` is the textual representation of data type (numpy-style).
    """
    if dtype[0] not in "<>":
        dtype=default_byteorder+dtype
    if dtype in idtypes_inv:
        return int(np.fromfile(f,dtype=dtype,count=1)[0])
    elif dtype in fdtypes_inv:
        return float(np.fromfile(f,dtype=dtype,count=1)[0])
    else:
        raise ValueError("unrecognized dtype: {}".format(dtype))
def read_str(f, dtype):
    """
    Read a string from file `f`.

    `dtype` is the textual representation of data type.
    Can be ``"sp"+sdtype`` (e.g., ``"sp<u2"``), where the string is prepended by its length written using ``sdtype`` format,
    or ``"s"+len`` (e.g., ``"s16"``), where ``len`` is the textual representation of string length (i.e., read ``len`` bytes and translate the result into string).
    """
    if dtype.startswith("sp"):
        sl=read_num(f,dtype[2:])
        return py3.as_str(f.read(sl))
    elif dtype.startswith("s"):
        sl=int(dtype[1:])
        return py3.as_str(f.read(sl))
    else:
        raise ValueError("unrecognized dtype: {}".format(dtype))
def read_pickle(f, dtype):
    """
    Read a value from file `f` as a Python pickle object.

    `dtype` is the textual representation of data type (numpy-style), and should be ``"pk"+proto+sdtype`` (e.g., ``"pk3<u2"``),
    where ``proto`` is the textual representation of the pickle protocol (ignored, added for compatibility with :func:`write_pickle`),
    and ``sdtype`` is the data type of the prepended string length (see ``"sp"+sdtype`` type in :func:`write_str`).
    """
    if dtype.startswith("pk"):
        sdtype=dtype[3:]
        v=read_str(f,"sp"+sdtype)
        return pickle.loads(v)
    else:
        raise ValueError("unrecognized dtype: {}".format(dtype))
def read_val(f, dtype):
    """
    Read an arbitrary value from file `f` using the supplied `dtype`.

    Storage type depends on `dtype`: can be string (see :func:`read_str`), number (see :func:`read_num`), or pickled value (see :func:`read_pickle`).
    In addition, `dtype` can be a tuple of dtypes with length equal to the length of `v`, in which case the values in `v` are read sequentially.
    """
    if isinstance(dtype,py3.textstring):
        if dtype.startswith("s"):
            return read_str(f,dtype)
        elif dtype.startswith("pk"):
            return read_pickle(f,dtype)
        else:
            return read_num(f,dtype)
    if isinstance(dtype,tuple):
        return tuple([ read_val(f,dt) for dt in dtype ])


@contextlib.contextmanager
def size_prepend(f, dtype, added=0):
    """
    Context manager that prepends the data written inside the block with its size (after the writing is done).

    `dtype` specifies size format; `added` is added to the size when saving.
    Note that this method requires back-seeking, so it doesn't work if the file is opened in append (``"a"``) mode;
    use ``"w"`` or ``"r+"`` mode instead.
    """
    spos=f.tell()
    write_num(0,f,dtype)
    bpos=f.tell()
    yield
    epos=f.tell()
    f.seek(spos)
    write_num(epos-bpos+added,f,dtype)
    f.seek(epos)