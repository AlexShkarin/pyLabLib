from ...core.utils import ctypes_wrap
from .misc import load_lib

import ctypes

from . import DCAM_lib_const as const


class DCAMLibError(RuntimeError):
    """Generic DCAM error."""
    def __init__(self, func, code):
        self.func=func
        self.code=code
        self.text_code,self.text_desc=const.DCAMERR.get(code,("UNKNOWN",""))
        msg="function '{}' raised error {} ({}): {}".format(func,code,self.text_code,self.text_desc)
        RuntimeError.__init__(self,msg)

def errcheck(passing=None):
    """
    Build an error checking function.

    Return a function which checks return codes of DCAM library functions.
    `passing` is a list specifying which return codes are acceptable (by default, non-negative codes are acceptable).
    """
    passing=set(passing) if passing is not None else set()
    def checker(result, func, arguments):
        if isinstance(result,tuple):
            code,result=result[0],result[1:]
        else:
            code=result
        if code<0 and code not in passing: # positive codes are always success
            raise DCAMLibError(func.__name__,code)
    return checker


class CSizePrepStruct(ctypes_wrap.StructWrap):
    _tup_exc={"size"}
    def prep(self, struct):
        struct.size=ctypes.sizeof(struct)
        return struct


class DCAM_GUID(ctypes.Structure):
	_fields_=[  ("Data1",ctypes.c_uint32),
				("Data2",ctypes.c_short),
				("Data3",ctypes.c_short),
				("Data4",ctypes.c_ubyte*8),
				("initoption",ctypes.POINTER(ctypes.c_int32)) ]
PDCAM_GUID=ctypes.POINTER(DCAM_GUID)

class DCAMAPI_INIT(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("iDeviceCount",ctypes.c_int32),
				("reserved",ctypes.c_int32),
				("initoptionbytes",ctypes.c_int32),
				("initoption",ctypes.POINTER(ctypes.c_int32)),
				("guid",PDCAM_GUID) ]
PDCAMAPI_INIT=ctypes.POINTER(DCAMAPI_INIT)
class CDCAMAPI_INIT(CSizePrepStruct):
    _struct=DCAMAPI_INIT
    _prep={ "initoption":ctypes_wrap.nullprep,
            "guid":ctypes_wrap.nullprep}

HDCAM=ctypes.c_void_p
HDCAMWAIT=ctypes.c_void_p

class DCAMDEV_OPEN(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("index",ctypes.c_int32),
				("hdcam",HDCAM) ]
PDCAMDEV_OPEN=ctypes.POINTER(DCAMDEV_OPEN)
class CDCAMDEV_OPEN(CSizePrepStruct):
    _struct=DCAMDEV_OPEN

class DCAMDEV_CAPABILITY(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("domain",ctypes.c_int32),
				("capflag",ctypes.c_int32),
				("kind",ctypes.c_int32) ]
PDCAMDEV_CAPABILITY=ctypes.POINTER(DCAMDEV_CAPABILITY)
class CDCAMDEV_CAPABILITY(CSizePrepStruct):
    _struct=DCAMDEV_CAPABILITY

DCAMDEV_STRING_MAXSIZE=512
class DCAMDEV_STRING(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("iString",ctypes.c_int32),
				("text",ctypes.c_char_p),
				("textbytes",ctypes.c_int32) ]
PDCAMDEV_STRING=ctypes.POINTER(DCAMDEV_STRING)
class CDCAMDEV_STRING(CSizePrepStruct):
    _struct=DCAMDEV_STRING
    _prep={"text":ctypes_wrap.strprep(DCAMDEV_STRING_MAXSIZE)}
    _default={"textbytes":DCAMDEV_STRING_MAXSIZE}

class DCAMDATA_HDR(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("iKind",ctypes.c_int32),
				("option",ctypes.c_int32),
				("reserved2",ctypes.c_int32) ]
PDCAMDATA_HDR=ctypes.POINTER(DCAMDATA_HDR)
class CDCAMDATA_HDR(CSizePrepStruct):
    _struct=DCAMDATA_HDR


class DCAMPROP_ATTR(ctypes.Structure):
	_fields_=[  ("cbSize",ctypes.c_int32),
				("iProp",ctypes.c_int32),
				("option",ctypes.c_int32),
				("iReserved1",ctypes.c_int32),
				("attribute",ctypes.c_int32),
				("iGroup",ctypes.c_int32),
				("iUnit",ctypes.c_int32),
				("attribute2",ctypes.c_int32),
				("valuemin",ctypes.c_double),
				("valuemax",ctypes.c_double),
				("valuestep",ctypes.c_double),
				("valuedefault",ctypes.c_double),
				("nMaxChannel",ctypes.c_int32),
				("iReserved3",ctypes.c_int32),
				("nMaxView",ctypes.c_int32),
				("iProp_NumberOfElement",ctypes.c_int32),
				("iProp_ArrayBase",ctypes.c_int32),
				("iPropStep_Element",ctypes.c_int32) ]
PDCAMPROP_ATTR=ctypes.POINTER(DCAMPROP_ATTR)
class CDCAMPROP_ATTR(ctypes_wrap.StructWrap):
    _struct=DCAMPROP_ATTR
    _tup_exc={"cbSize","iReserved1","iGroup","iReserved3","option"}
    def prep(self, struct):
        struct.cbSize=ctypes.sizeof(struct)
        return struct

DCAMPROP_VALUETEXT_MAXSIZE=512
class DCAMPROP_VALUETEXT(ctypes.Structure):
	_fields_=[  ("cbSize",ctypes.c_int32),
				("iProp",ctypes.c_int32),
                ("value",ctypes.c_double),
				("text",ctypes.c_char_p),
				("textbytes",ctypes.c_int32) ]
PDCAMPROP_VALUETEXT=ctypes.POINTER(DCAMPROP_VALUETEXT)
class CDCAMPROP_VALUETEXT(ctypes_wrap.StructWrap):
    _struct=DCAMPROP_VALUETEXT
    _prep={"text":ctypes_wrap.strprep(DCAMPROP_VALUETEXT_MAXSIZE)}
    _default={"textbytes":DCAMPROP_VALUETEXT_MAXSIZE}
    def prep(self, struct):
        struct.cbSize=ctypes.sizeof(struct)
        return struct

class DCAM_TIMESTAMP(ctypes.Structure):
	_fields_=[  ("sec",ctypes.c_uint32),
				("microsec",ctypes.c_int32) ]
PDCAM_TIMESTAMP=ctypes.POINTER(DCAM_TIMESTAMP)
class CDCAM_TIMESTAMP(ctypes_wrap.StructWrap):
    _struct=DCAM_TIMESTAMP

class DCAMBUF_FRAME(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("iKind",ctypes.c_int32),
                ("option",ctypes.c_int32),
                ("iFrame",ctypes.c_int32),
                ("buf",ctypes.c_void_p),
                ("rowbytes",ctypes.c_int32),
                ("pixeltype",ctypes.c_uint32),
                ("width",ctypes.c_int32),
                ("height",ctypes.c_int32),
                ("left",ctypes.c_int32),
                ("top",ctypes.c_int32),
                ("timestamp",DCAM_TIMESTAMP),
                ("framestamp",ctypes.c_int32),
                ("camerastamp",ctypes.c_int32) ]
PDCAMBUF_FRAME=ctypes.POINTER(DCAMBUF_FRAME)
class CDCAMBUF_FRAME(CSizePrepStruct):
    _struct=DCAMBUF_FRAME
    _conv={ "timestamp":CDCAM_TIMESTAMP.tup_struct}
    _prep={ "buf":ctypes_wrap.nullprep }
    _tup_exc={"size","iKind","option"}
    _tup_add={"bpp","btot"}
    def conv(self):
        self.bpr=abs(self.rowbytes)
        self.bpp=self.bpr/float(self.width) if self.width else None
        self.btot=self.bpr*abs(self.height)

class DCAMCAP_TRANSFERINFO(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("iKind",ctypes.c_int32),
                ("nNewestFrameIndex",ctypes.c_int32),
                ("nFrameCount",ctypes.c_int32) ]
PDCAMCAP_TRANSFERINFO=ctypes.POINTER(DCAMCAP_TRANSFERINFO)
class CDCAMCAP_TRANSFERINFO(CSizePrepStruct):
    _struct=DCAMCAP_TRANSFERINFO
    _tup_exc={"size","iKind"}

class DCAMWAIT_OPEN(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("supportevent",ctypes.c_int32),
                ("hwait",HDCAMWAIT),
                ("hdcam",HDCAM) ]
PDCAMWAIT_OPEN=ctypes.POINTER(DCAMWAIT_OPEN)
class CDCAMWAIT_OPEN(CSizePrepStruct):
    _struct=DCAMWAIT_OPEN
    _tup_exc={"size","hdcam"}
    
class DCAMWAIT_START(ctypes.Structure):
	_fields_=[  ("size",ctypes.c_int32),
				("eventhappened",ctypes.c_int32),
                ("eventmask",ctypes.c_int32),
                ("timeout",ctypes.c_int32) ]
PDCAMWAIT_START=ctypes.POINTER(DCAMWAIT_START)
class CDCAMWAIT_START(CSizePrepStruct):
    _struct=DCAMWAIT_START

class DCAMLib(object):
    def __init__(self):
        object.__init__(self)
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return
        error_message="The library is automatically supplied with Hamamatsu HOKAWO or DCAM-API software"
        self.lib=load_lib("dcamapi.dll",error_message=error_message,call_conv="stdcall")
        lib=self.lib

        wrapper=ctypes_wrap.CTypesWrapper(restype=ctypes.c_int, return_res=False, errcheck=errcheck())

        self.dcamapi_init=wrapper(lib.dcamapi_init, [DCAMAPI_INIT], [None], rvprep=[CDCAMAPI_INIT.prep_struct], rvconv=[lambda s: CDCAMAPI_INIT(s).iDeviceCount],)
        self.dcamapi_uninit=wrapper(lib.dcamapi_uninit)

        def dcamdev_open_prep(index):
            cstruct=CDCAMDEV_OPEN()
            cstruct.index=index
            return cstruct.to_struct()
        self.dcamdev_open=wrapper(lib.dcamdev_open, [DCAMDEV_OPEN], [None], addargs=["index"], rvprep=[dcamdev_open_prep], rvconv=[lambda s, *args: CDCAMDEV_OPEN(s).hdcam])
        self.dcamdev_close=wrapper(lib.dcamdev_close, [HDCAM], ["hdcam"])

        def dcamdev_getcapability_prep(_, domain, kind):
            cstruct=CDCAMDEV_CAPABILITY()
            cstruct.domain=domain
            cstruct.kind=kind
            return cstruct.to_struct()
        self.dcamdev_getcapability=wrapper(lib.dcamdev_getcapability, [HDCAM, DCAMDEV_CAPABILITY], ["hdcam", None], addargs=["domain","kind"], rvprep=[dcamdev_getcapability_prep], rvconv=[lambda s, *args: CDCAMDEV_CAPABILITY(s).capflag])

        def dcamdev_getstring_prep(_, iString):
            cstruct=CDCAMDEV_STRING()
            cstruct.iString=iString
            return cstruct.to_struct()
        self.dcamdev_getstring=wrapper(lib.dcamdev_getstring, [HDCAM, DCAMDEV_STRING], ["hdcam", None], addargs=["iString"], rvprep=[dcamdev_getstring_prep], rvconv=[lambda s, *args: ctypes.string_at(CDCAMDEV_STRING(s).text)])
        
        def dcamprop_getattr_prep(_, iProp):
            cstruct=CDCAMPROP_ATTR()
            cstruct.iProp=iProp
            return cstruct.to_struct()
        self.dcamprop_getattr=wrapper(lib.dcamprop_getattr, [HDCAM, DCAMPROP_ATTR], ["hdcam", None], addargs=["iProp"], rvprep=[dcamprop_getattr_prep], rvconv=[CDCAMPROP_ATTR.tup_struct])
        self.dcamprop_getvalue=wrapper(lib.dcamprop_getvalue, [HDCAM, ctypes.c_int32, ctypes.c_double], ["hdcam", "iProp", None])
        self.dcamprop_setvalue=wrapper(lib.dcamprop_setvalue, [HDCAM, ctypes.c_int32, ctypes.c_double], ["hdcam", "iProp", "fValue"])
        self.dcamprop_setgetvalue_lib=wrapper(lib.dcamprop_setgetvalue, [HDCAM, ctypes.c_int32, ctypes.c_double, ctypes.c_int32], ["hdcam", "iProp", None, "option"], addargs=["fValue"], rvprep=[lambda *args: ctypes.c_double(args[-1])])
        self.dcamprop_queryvalue_lib=wrapper(lib.dcamprop_queryvalue, [HDCAM, ctypes.c_int32, ctypes.c_double, ctypes.c_int32], ["hdcam", "iProp", None, "option"], addargs=["fValue"], rvprep=[lambda *args: ctypes.c_double(args[-1])])
        self.dcamprop_getnextid_lib=wrapper(lib.dcamprop_getnextid, [HDCAM, ctypes.c_int32, ctypes.c_int32], ["hdcam", None, "option"], addargs=["pProp"], rvprep=[lambda *args: ctypes.c_int32(args[-1])])
        self.dcamprop_getname_lib=wrapper(lib.dcamprop_getname, [HDCAM, ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32], ["hdcam", "iProp", None, "textbytes"],rvprep=[ctypes_wrap.strprep(DCAMDEV_STRING_MAXSIZE)],rvref=[False])
        def dcamprop_getvaluetext_prep(_, iProp, value):
            cstruct=CDCAMPROP_VALUETEXT()
            cstruct.iProp=iProp
            cstruct.value=value
            return cstruct.to_struct()
        self.dcamprop_getvaluetext=wrapper(lib.dcamprop_getvaluetext, [HDCAM, DCAMPROP_VALUETEXT], ["hdcam", None], addargs=["iProp","value"], rvprep=[dcamprop_getvaluetext_prep], rvconv=[lambda s, *args: ctypes.string_at(CDCAMPROP_VALUETEXT(s).text)])

        self.dcambuf_alloc=wrapper(lib.dcambuf_alloc, [HDCAM, ctypes.c_int32], ["hdcam", "framecount"])
        self.dcambuf_release=wrapper(lib.dcambuf_release, [HDCAM, ctypes.c_int32], ["hdcam", "iKind"])
        def dcambuf_lockframe_prep(_, iFrame):
            cstruct=CDCAMBUF_FRAME()
            cstruct.iFrame=iFrame
            return cstruct.to_struct()
        self.dcambuf_lockframe=wrapper(lib.dcambuf_lockframe, [HDCAM, DCAMBUF_FRAME], ["hdcam", None], addargs=["iFrame"], rvprep=[dcambuf_lockframe_prep], rvconv=[CDCAMBUF_FRAME.tup_struct])
        self.dcamcap_start=wrapper(lib.dcamcap_start, [HDCAM, ctypes.c_int32], ["hdcam", "mode"])
        self.dcamcap_stop=wrapper(lib.dcamcap_stop, [HDCAM], ["hdcam"])
        self.dcamcap_status=wrapper(lib.dcamcap_status, [HDCAM, ctypes.c_int32], ["hdcam", None])
        def dcamcap_transferinfo_prep(_, iKind):
            cstruct=CDCAMCAP_TRANSFERINFO()
            cstruct.iKind=iKind
            return cstruct.to_struct()
        self.dcamcap_transferinfo=wrapper(lib.dcamcap_transferinfo, [HDCAM, DCAMCAP_TRANSFERINFO], ["hdcam", None], addargs=["iKind"], rvprep=[dcamcap_transferinfo_prep], rvconv=[CDCAMCAP_TRANSFERINFO.tup_struct])
        self.dcamcap_firetrigger_lib=wrapper(lib.dcamcap_firetrigger, [HDCAM, ctypes.c_int32], ["hdcam", "iKind"])

        def dcamwait_open_prep(hdcam):
            cstruct=CDCAMWAIT_OPEN()
            cstruct.hdcam=hdcam
            return cstruct.to_struct()
        self.dcamwait_open=wrapper(lib.dcamwait_open, [DCAMWAIT_OPEN], [None], addargs=["hdcam"], rvprep=[dcamwait_open_prep], rvconv=[CDCAMWAIT_OPEN.tup_struct])
        self.dcamwait_close=wrapper(lib.dcamwait_close, [HDCAMWAIT], ["hwait"])
        def dcamwait_start_prep(_, eventmask, timeout):
            cstruct=CDCAMWAIT_START()
            cstruct.eventhappened=0
            cstruct.eventmask=eventmask
            cstruct.timeout=timeout
            return cstruct.to_struct()
        self.dcamwait_start=wrapper(lib.dcamwait_start, [HDCAMWAIT, DCAMWAIT_START], ["hwait", None], addargs=["eventmask","timeout"], rvprep=[dcamwait_start_prep], rvconv=[lambda s, *args: CDCAMWAIT_START(s).eventhappened])
        self.dcamwait_abort=wrapper(lib.dcamwait_abort, [HDCAMWAIT], ["hwait"])

        self._initialized=True

    def dcamprop_setgetvalue(self, hdcam, iProp, fValue):
        return self.dcamprop_setgetvalue_lib(hdcam,iProp,0,fValue)
    def dcamprop_queryvalue(self, hdcam, iProp, fValue, option):
        return self.dcamprop_queryvalue_lib(hdcam,iProp,option,fValue)
    def dcamprop_getnextid(self, hdcam, iProp, option):
        return self.dcamprop_getnextid_lib(hdcam,option,iProp)
    def dcamprop_getallids(self, hdcam, option):
        ids=[]
        iProp=0
        while True:
            try:
                iProp=self.dcamprop_getnextid(hdcam,iProp,option)
            except DCAMLibError as e:
                if e.code==-2147481560:
                    break
                raise
            if iProp==0 or iProp in ids:
                break
            ids.append(iProp)
        return ids
    def dcamprop_getname(self, hdcam, iProp):
        return self.dcamprop_getname_lib(hdcam,iProp,DCAMDEV_STRING_MAXSIZE)
    def dcamcap_firetrigger(self, hdcam):
        return self.dcamcap_firetrigger_lib(hdcam,0)

lib=DCAMLib()