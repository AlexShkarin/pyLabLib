# pylint: disable=wrong-spelling-in-comment

from . import dcamprop_defs, dcamapi4_defs  # pylint: disable=unused-import
from .dcamapi4_defs import DCAMAPI_INIT, DCAMDEV_OPEN, DCAMDEV_CAPABILITY
from .dcamapi4_defs import DCAMDEV_STRING, DCAMDATA_HDR
from .dcamapi4_defs import DCAMPROP_ATTR, DCAMPROP_VALUETEXT
from .dcamapi4_defs import CDCAM_TIMESTAMP
from .dcamapi4_defs import DCAMBUF_FRAME, DCAMWAIT_OPEN, DCAMWAIT_START, DCAMCAP_TRANSFERINFO
from .dcamapi4_defs import DCAMERR, drDCAMERR, define_functions
from .dcamapi4_defs import DCAMCAP_STATUS, DCAMWAIT_EVENT, DCAM_IDSTR  # pylint: disable=unused-import

from ...core.utils import ctypes_wrap
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib
import ctypes



class DCAMError(DeviceError):
    """Generic DCAM error"""
class DCAMLibError(DCAMError):
    """Generic DCAM library error"""
    def __init__(self, func, code):
        self.func=func
        self.code=code
        self.name=drDCAMERR.get(self.code,"UNKNOWN")
        msg="function '{}' raised error {} ({})".format(func,code,self.name)
        DCAMError.__init__(self,msg)

def errcheck(passing=None):
    """
    Build an error checking function.

    Return a function which checks return codes of DCAM library functions.
    `passing` is a list specifying which return codes are acceptable (by default, non-negative codes are acceptable).
    """
    passing=set(passing) if passing is not None else set()
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if isinstance(result,tuple):
            code,result=result[0],result[1:]
        else:
            code=result
        if code<0 and code not in passing: # positive codes are always success
            raise DCAMLibError(func.__name__,code)
    return errchecker





class CSizePrepStruct(ctypes_wrap.CStructWrapper):
    _tup_exc={"size"}
    def prep(self, struct):
        struct.size=ctypes.sizeof(struct)
        return struct

class CDCAMAPI_INIT(CSizePrepStruct):
    _struct=DCAMAPI_INIT
    _prep={ "initoption":None,
            "guid":None}

class CDCAMDEV_OPEN(CSizePrepStruct):
    _struct=DCAMDEV_OPEN

class CDCAMDEV_CAPABILITY(CSizePrepStruct):
    _struct=DCAMDEV_CAPABILITY

DCAMDEV_STRING_MAXSIZE=512
class CDCAMDEV_STRING(CSizePrepStruct):
    _struct=DCAMDEV_STRING
    _prep={"text":ctypes_wrap.strprep(DCAMDEV_STRING_MAXSIZE), "textbytes":DCAMDEV_STRING_MAXSIZE}

class CDCAMDATA_HDR(CSizePrepStruct):
    _struct=DCAMDATA_HDR

class CDCAMPROP_ATTR(ctypes_wrap.CStructWrapper):
    _struct=DCAMPROP_ATTR
    _tup_exc={"cbSize","iReserved1","iGroup","iReserved3","option"}
    def prep(self, struct):
        struct.cbSize=ctypes.sizeof(struct)
        return struct

DCAMPROP_VALUETEXT_MAXSIZE=512
class CDCAMPROP_VALUETEXT(ctypes_wrap.CStructWrapper):
    _struct=DCAMPROP_VALUETEXT
    _prep={"text":ctypes_wrap.strprep(DCAMPROP_VALUETEXT_MAXSIZE), "textbytes":DCAMPROP_VALUETEXT_MAXSIZE}
    def prep(self, struct):
        struct.cbSize=ctypes.sizeof(struct)
        return struct

class CDCAMBUF_FRAME(CSizePrepStruct):
    _struct=DCAMBUF_FRAME
    _conv={ "timestamp":CDCAM_TIMESTAMP.tup_struct}
    _prep={ "buf":None }
    _tup_exc={"size","iKind","option"}
    _tup_add={"bpp","btot"}
    def conv(self):
        self.bpr=abs(self.rowbytes) # pylint: disable=no-member
        self.bpp=self.bpr/float(self.width) if self.width else None # pylint: disable=no-member
        self.btot=self.bpr*abs(self.height) # pylint: disable=no-member

class CDCAMCAP_TRANSFERINFO(CSizePrepStruct):
    _struct=DCAMCAP_TRANSFERINFO
    _tup_exc={"size","iKind"}

class CDCAMWAIT_OPEN(CSizePrepStruct):
    _struct=DCAMWAIT_OPEN
    _tup_exc={"size","hdcam"}
    
class CDCAMWAIT_START(CSizePrepStruct):
    _struct=DCAMWAIT_START



class DCAMLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with Hamamatsu HOKAWO or DCAM-API software\n"+load_lib.par_error_message.format("dcamapi")
        self.lib=load_lib.load_lib("dcamapi.dll",locations=("parameter/dcamapi","global"),error_message=error_message,call_conv="cdecl")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck())

        #  ctypes.c_int dcamapi_init(ctypes.POINTER(DCAMAPI_INIT) param)
        self.dcamapi_init=wrapper(lib.dcamapi_init, rvals=["param"],
            argprep={"param":CDCAMAPI_INIT.prep_struct}, rconv={"param":lambda s: CDCAMAPI_INIT(s).iDeviceCount}) # pylint: disable=no-member
        #  ctypes.c_int dcamapi_uninit()
        self.dcamapi_uninit=wrapper(lib.dcamapi_uninit)

        #  ctypes.c_int dcamdev_open(ctypes.POINTER(DCAMDEV_OPEN) param)
        def dcamdev_open_prep(index):
            return CDCAMDEV_OPEN.prep_struct_args(index=index)
        self.dcamdev_open=wrapper(lib.dcamdev_open, args=["index"], rvals=["param"],
            argprep={"param":dcamdev_open_prep}, rconv={"param":lambda s: CDCAMDEV_OPEN(s).hdcam}) # pylint: disable=no-member
        #  ctypes.c_int dcamdev_close(HDCAM h)
        self.dcamdev_close=wrapper(lib.dcamdev_close)
        
        #  ctypes.c_int dcamdev_getcapability(HDCAM h, ctypes.POINTER(DCAMDEV_CAPABILITY) param)
        def dcamdev_getcapability_prep(domain, kind):
            return CDCAMDEV_CAPABILITY.prep_struct_args(domain=domain,kind=kind)
        self.dcamdev_getcapability=wrapper(lib.dcamdev_getcapability, args=["h","domain","kind"], rvals=["param"],
            argprep={"param":dcamdev_getcapability_prep}, rconv={"param":lambda s: CDCAMDEV_CAPABILITY(s).capflag}) # pylint: disable=no-member
        
        #  ctypes.c_int dcamdev_getstring(HDCAM h, ctypes.POINTER(DCAMDEV_STRING) param)
        def dcamdev_getstring_prep(iString):
            return CDCAMDEV_STRING.prep_struct_args(iString=iString)
        self.dcamdev_getstring=wrapper(lib.dcamdev_getstring, args=["h","iString"], rvals=["param"],
            argprep={"param":dcamdev_getstring_prep}, rconv={"param":lambda s: ctypes.string_at(CDCAMDEV_STRING(s).text)}) # pylint: disable=no-member
        #  ctypes.c_int dcamprop_getattr(HDCAM h, ctypes.POINTER(DCAMPROP_ATTR) param)
        def dcamprop_getattr_prep(iProp):
            return CDCAMPROP_ATTR.prep_struct_args(iProp=iProp)
        self.dcamprop_getattr=wrapper(lib.dcamprop_getattr, args=["h","iProp"], rvals=["param"],
            argprep={"param":dcamprop_getattr_prep}, rconv={"param":CDCAMPROP_ATTR.tup_struct})
        #  ctypes.c_int dcamprop_getvalue(HDCAM h, int32 iProp, ctypes.POINTER(ctypes.c_double) pValue)
        self.dcamprop_getvalue=wrapper(lib.dcamprop_getvalue, rvals=["pValue"])
        #  ctypes.c_int dcamprop_setvalue(HDCAM h, int32 iProp, ctypes.c_double fValue)
        self.dcamprop_setvalue=wrapper(lib.dcamprop_setvalue)
        #  ctypes.c_int dcamprop_setgetvalue(HDCAM h, int32 iProp, ctypes.POINTER(ctypes.c_double) pValue, int32 option)
        self.dcamprop_setgetvalue_lib=wrapper(lib.dcamprop_setgetvalue, args="all", rvals=["pValue"])
        #  ctypes.c_int dcamprop_queryvalue(HDCAM h, int32 iProp, ctypes.POINTER(ctypes.c_double) pValue, int32 option)
        self.dcamprop_queryvalue=wrapper(lib.dcamprop_queryvalue, args="all", rvals=["pValue"])
        #  ctypes.c_int dcamprop_getnextid(HDCAM h, ctypes.POINTER(int32) pProp, int32 option)
        self.dcamprop_getnextid=wrapper(lib.dcamprop_getnextid, args="all", rvals=["pProp"])
        #  ctypes.c_int dcamprop_getname(HDCAM h, int32 iProp, ctypes.c_char_p text, int32 textbytes)
        self.dcamprop_getname=wrapper(lib.dcamprop_getname, args=["h","iProp"], rvals=["text"], byref=[],
            argprep={"textbytes":DCAMDEV_STRING_MAXSIZE,"text":ctypes_wrap.strprep(DCAMDEV_STRING_MAXSIZE)})
        #  ctypes.c_int dcamprop_getvaluetext(HDCAM h, ctypes.POINTER(DCAMPROP_VALUETEXT) param)
        def dcamprop_getvaluetext_prep(iProp, value):
            return CDCAMPROP_VALUETEXT.prep_struct_args(iProp=iProp,value=value)
        self.dcamprop_getvaluetext=wrapper(lib.dcamprop_getvaluetext, args=["h","iProp","value"], rvals=["param"],
            argprep={"param":dcamprop_getvaluetext_prep}, rconv={"param":lambda s: ctypes.string_at(CDCAMPROP_VALUETEXT(s).text)}) # pylint: disable=no-member
        #  ctypes.c_int dcamdev_setdata(HDCAM h, ctypes.POINTER(DCAMDATA_HDR) param)
        self.dcamdev_setdata=wrapper(lib.dcamdev_setdata, args="all", rvals=["param"])
        #  ctypes.c_int dcamdev_getdata(HDCAM h, ctypes.POINTER(DCAMDATA_HDR) param)
        self.dcamdev_getdata=wrapper(lib.dcamdev_getdata, args="all", rvals=["param"])
        
        #  ctypes.c_int dcamcap_start(HDCAM h, int32 mode)
        self.dcamcap_start=wrapper(lib.dcamcap_start)
        #  ctypes.c_int dcamcap_stop(HDCAM h)
        self.dcamcap_stop=wrapper(lib.dcamcap_stop)
        #  ctypes.c_int dcamcap_status(HDCAM h, ctypes.POINTER(int32) pStatus)
        self.dcamcap_status=wrapper(lib.dcamcap_status, rvals=["pStatus"])
        #  ctypes.c_int dcamcap_transferinfo(HDCAM h, ctypes.POINTER(DCAMCAP_TRANSFERINFO) param)
        def dcamcap_transferinfo_prep(iKind):
            return CDCAMCAP_TRANSFERINFO.prep_struct_args(iKind=iKind)
        self.dcamcap_transferinfo=wrapper(lib.dcamcap_transferinfo, args=["h","iKind"], rvals=["param"],
            argprep={"param":dcamcap_transferinfo_prep}, rconv={"param":CDCAMCAP_TRANSFERINFO.tup_struct})
        #  ctypes.c_int dcamcap_firetrigger(HDCAM h, int32 iKind)
        self.dcamcap_firetrigger_lib=wrapper(lib.dcamcap_firetrigger)

        #  ctypes.c_int dcamwait_open(ctypes.POINTER(DCAMWAIT_OPEN) param)
        def dcamwait_open_prep(hdcam):
            return CDCAMWAIT_OPEN.prep_struct_args(hdcam=hdcam)
        self.dcamwait_open=wrapper(lib.dcamwait_open, args=["hdcam"], rvals=["param"],
            argprep={"param":dcamwait_open_prep}, rconv={"param":CDCAMWAIT_OPEN.tup_struct})
        #  ctypes.c_int dcamwait_close(HDCAMWAIT hWait)
        self.dcamwait_close=wrapper(lib.dcamwait_close)
        #  ctypes.c_int dcamwait_start(HDCAMWAIT hWait, ctypes.POINTER(DCAMWAIT_START) param)
        def dcamwait_start_prep(eventmask, timeout):
            return CDCAMWAIT_START.prep_struct_args(eventmask=eventmask,timeout=timeout,eventhappened=0)
        self.dcamwait_start=wrapper(lib.dcamwait_start, args=["hWait","eventmask","timeout"], rvals=["param"],
            argprep={"param":dcamwait_start_prep}, rconv={"param":lambda s: CDCAMWAIT_START(s).eventhappened}) # pylint: disable=no-member
        #  ctypes.c_int dcamwait_abort(HDCAMWAIT hWait)
        self.dcamwait_abort=wrapper(lib.dcamwait_abort)

        #  ctypes.c_int dcambuf_alloc(HDCAM h, int32 framecount)
        self.dcambuf_alloc=wrapper(lib.dcambuf_alloc)
        #  ctypes.c_int dcambuf_release(HDCAM h, int32 iKind)
        self.dcambuf_release=wrapper(lib.dcambuf_release)
        #  ctypes.c_int dcambuf_lockframe(HDCAM h, ctypes.POINTER(DCAMBUF_FRAME) pFrame)
        def dcambuf_lockframe_prep(iFrame):
            return CDCAMBUF_FRAME.prep_struct_args(iFrame=iFrame)
        self.dcambuf_lockframe=wrapper(lib.dcambuf_lockframe, args=["h","iFrame"], rvals=["pFrame"],
            argprep={"pFrame":dcambuf_lockframe_prep}, rconv={"pFrame":CDCAMBUF_FRAME.tup_struct})

        self._initialized=True



    def dcamprop_setgetvalue(self, hdcam, iProp, fValue, option=0):
        return self.dcamprop_setgetvalue_lib(hdcam,iProp,fValue,option)
    def dcamcap_firetrigger(self, hdcam, iKind=0):
        return self.dcamcap_firetrigger_lib(hdcam,iKind)
    def dcamprop_getallids(self, hdcam, option):
        ids=[]
        iProp=0
        while True:
            try:
                iProp=self.dcamprop_getnextid(hdcam,iProp,option)
            except DCAMLibError as e:
                if e.code==DCAMERR.DCAMERR_NOPROPERTY:
                    break
                raise
            if iProp==0 or iProp in ids:
                break
            ids.append(iProp)
        return ids



wlib=DCAMLib()