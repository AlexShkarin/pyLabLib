# pylint: disable=wrong-spelling-in-comment

from . import pvcam_defs
from .pvcam_defs import define_functions, PARAM_TYPE, PL_PARAM_ATTRIBUTES

from ...core.utils import ctypes_wrap, py3
from ...core.devio.comm_backend import DeviceError
from ..utils import load_lib

import platform
import ctypes


class PvcamError(DeviceError):
    """Generic Pvcam error"""
class PvcamLibError(PvcamError):
    """Generic Pvcam library error"""
    def __init__(self, func, lib=None):
        self.func=func
        self.code=None
        self.desc=None
        if lib is not None:
            self.code=lib.pl_error_code()
            try:
                self.desc=py3.as_str(lib.pl_error_message(self.code))
            except PvcamError:
                pass
            descstr="" if self.desc is None else ": {}".format(self.desc)
            self.msg="function '{}' raised error {}{}".format(func,self.code,descstr)
        else:
            self.msg="function '{}' raised error".format(func)
        super().__init__(self.msg)
def errcheck(lib=None):
    """
    Build an error checking function.

    Return a function which checks return codes of Pvcam library functions.
    """
    def errchecker(result, func, arguments):  # pylint: disable=unused-argument
        if result==0:  # PV_FAIL
            raise PvcamLibError(func.__name__,lib=lib)
        return result
    return errchecker


class CFRAME_INFO(pvcam_defs.CFRAME_INFO):
    _tup={"FrameInfoGUID":pvcam_defs.CPVCAM_FRAME_INFO_GUID.tup_struct}

class Cmd_frame_header(pvcam_defs.Cmd_frame_header):
    _tup_exc=["_reserved"]
class Cmd_frame_header_v3(pvcam_defs.Cmd_frame_header_v3):
    _tup_exc=["_reserved"]
class Cmd_frame_roi_header(pvcam_defs.Cmd_frame_roi_header):
    _tup_exc=["_reserved"]
    _tup={"roi":pvcam_defs.Crgn_type.tup_struct}


class PvcamLib:
    def __init__(self):
        self._initialized=False

    def initlib(self):
        if self._initialized:
            return

        error_message="The library is supplied with Photometrics PVCAM software\n"+load_lib.par_error_message.format("pvcam")
        archbit=platform.architecture()[0][:2]
        lib_name="pvcam{}.dll".format(archbit)
        self.lib=load_lib.load_lib(lib_name,locations=("parameter/pvcam","global"),error_message=error_message,call_conv="stdcall")
        lib=self.lib
        define_functions(lib)

        wrapper=ctypes_wrap.CFunctionWrapper(errcheck=errcheck(lib=self),default_rvals="pointer")
        strprep=ctypes_wrap.strprep(64)
        longstrprep=ctypes_wrap.strprep(2048)

        #  int16 pl_error_code()
        self.pl_error_code=ctypes_wrap.CFunctionWrapper()(lib.pl_error_code)
        #  rs_bool pl_error_message(int16 err_code, ctypes.c_char_p msg)
        self.pl_error_message=ctypes_wrap.CFunctionWrapper(errcheck=errcheck())(lib.pl_error_message, rvals=["msg"],
            argprep={"msg":longstrprep}, byref=[])

        #  rs_bool pl_pvcam_get_ver(ctypes.POINTER(uns16) pvcam_version)
        self.pl_pvcam_get_ver=wrapper(lib.pl_pvcam_get_ver)
        #  rs_bool pl_pvcam_init()
        self.pl_pvcam_init=wrapper(lib.pl_pvcam_init)
        #  rs_bool pl_pvcam_uninit()
        self.pl_pvcam_uninit=wrapper(lib.pl_pvcam_uninit)
        #  rs_bool pl_cam_get_total(ctypes.POINTER(int16) totl_cams)
        self.pl_cam_get_total=wrapper(lib.pl_cam_get_total)
        #  rs_bool pl_cam_get_name(int16 cam_num, ctypes.c_char_p camera_name)
        self.pl_cam_get_name=wrapper(lib.pl_cam_get_name, rvals=["camera_name"],
            argprep={"camera_name":strprep}, byref=[])
        #  rs_bool pl_cam_open(ctypes.c_char_p camera_name, ctypes.POINTER(int16) hcam, int16 o_mode)
        self.pl_cam_open=wrapper(lib.pl_cam_open)
        #  rs_bool pl_cam_close(int16 hcam)
        self.pl_cam_close=wrapper(lib.pl_cam_close)

        #  rs_bool pl_get_param(int16 hcam, uns32 param_id, int16 param_attribute, ctypes.c_void_p param_value)
        self.pl_get_param=wrapper(lib.pl_get_param)
        #  rs_bool pl_set_param(int16 hcam, uns32 param_id, ctypes.c_void_p param_value)
        self.pl_set_param=wrapper(lib.pl_set_param)
        #  rs_bool pl_get_enum_param(int16 hcam, uns32 param_id, uns32 index, ctypes.POINTER(int32) value, ctypes.c_char_p desc, uns32 length)
        self.pl_get_enum_param=wrapper(lib.pl_get_enum_param)
        #  rs_bool pl_enum_str_length(int16 hcam, uns32 param_id, uns32 index, ctypes.POINTER(uns32) length)
        self.pl_enum_str_length=wrapper(lib.pl_enum_str_length)

        #  rs_bool pl_create_frame_info_struct(ctypes.POINTER(ctypes.POINTER(FRAME_INFO)) new_frame)
        self.pl_create_frame_info_struct=wrapper(lib.pl_create_frame_info_struct)
        #  rs_bool pl_release_frame_info_struct(ctypes.POINTER(FRAME_INFO) frame_to_delete)
        self.pl_release_frame_info_struct=wrapper(lib.pl_release_frame_info_struct, args="all", byref=[])
        #  rs_bool pl_create_smart_stream_struct(ctypes.POINTER(ctypes.POINTER(smart_stream_type)) array, uns16 entries)
        self.pl_create_smart_stream_struct=wrapper(lib.pl_create_smart_stream_struct)
        #  rs_bool pl_release_smart_stream_struct(ctypes.POINTER(ctypes.POINTER(smart_stream_type)) array)
        self.pl_release_smart_stream_struct=wrapper(lib.pl_release_smart_stream_struct, args="all", byref=[])

       #  rs_bool pl_exp_trigger(int16 hcam, ctypes.POINTER(uns32) flags, uns32 value)
        self.pl_exp_trigger=wrapper(lib.pl_exp_trigger)
        
        #  rs_bool pl_exp_setup_seq(int16 hcam, uns16 exp_total, uns16 rgn_total, ctypes.POINTER(rgn_type) rgn_array, int16 exp_mode, uns32 exposure_time, ctypes.POINTER(uns32) exp_bytes)
        self.pl_exp_setup_seq_lib=wrapper(lib.pl_exp_setup_seq, args=["hcam", "exp_total", "rgn_total", "rgn_array", "exp_mode", "exposure_time"],
            rvals=["exp_bytes"], byref=["exp_bytes"])
        #  rs_bool pl_exp_start_seq(int16 hcam, ctypes.c_void_p pixel_stream)
        self.pl_exp_start_seq=wrapper(lib.pl_exp_start_seq)
        #  rs_bool pl_exp_check_status(int16 hcam, ctypes.POINTER(int16) status, ctypes.POINTER(uns32) bytes_arrived)
        self.pl_exp_check_status=wrapper(lib.pl_exp_check_status)
        #  rs_bool pl_exp_finish_seq(int16 hcam, ctypes.c_void_p pixel_stream, int16 hbuf)
        self.pl_exp_finish_seq=wrapper(lib.pl_exp_finish_seq)

        #  rs_bool pl_exp_setup_cont(int16 hcam, uns16 rgn_total, ctypes.POINTER(rgn_type) rgn_array, int16 exp_mode, uns32 exposure_time, ctypes.POINTER(uns32) exp_bytes, int16 buffer_mode)
        self.pl_exp_setup_cont_lib=wrapper(lib.pl_exp_setup_cont, args=["hcam", "rgn_total", "rgn_array", "exp_mode", "exposure_time", "buffer_mode"],
            rvals=["exp_bytes"], byref=["exp_bytes"])
        #  rs_bool pl_exp_start_cont(int16 hcam, ctypes.c_void_p pixel_stream, uns32 size)
        self.pl_exp_start_cont=wrapper(lib.pl_exp_start_cont)
        #  rs_bool pl_exp_check_cont_status(int16 hcam, ctypes.POINTER(int16) status, ctypes.POINTER(uns32) bytes_arrived, ctypes.POINTER(uns32) buffer_cnt)
        self.pl_exp_check_cont_status=wrapper(lib.pl_exp_check_cont_status)
        #  rs_bool pl_exp_check_cont_status_ex(int16 hcam, ctypes.POINTER(int16) status, ctypes.POINTER(uns32) byte_cnt, ctypes.POINTER(uns32) buffer_cnt, ctypes.POINTER(FRAME_INFO) frame_info)
        self.pl_exp_check_cont_status_ex_lib=wrapper(lib.pl_exp_check_cont_status_ex, args=["hcam","frame_info"], rvals="rest", byref=["status","byte_cnt","buffer_cnt"])
        #  rs_bool pl_exp_stop_cont(int16 hcam, int16 cam_state)
        self.pl_exp_stop_cont=wrapper(lib.pl_exp_stop_cont)
        #  rs_bool pl_exp_abort(int16 hcam, int16 cam_state)
        self.pl_exp_abort=wrapper(lib.pl_exp_abort)
        
        #  rs_bool pl_exp_get_latest_frame(int16 hcam, ctypes.POINTER(ctypes.c_void_p) frame)
        self.pl_exp_get_latest_frame=wrapper(lib.pl_exp_get_latest_frame)
        #  rs_bool pl_exp_get_latest_frame_ex(int16 hcam, ctypes.POINTER(ctypes.c_void_p) frame, ctypes.POINTER(FRAME_INFO) frame_info)
        self.pl_exp_get_latest_frame_ex_lib=wrapper(lib.pl_exp_get_latest_frame_ex, args=["hcam","frame_info"], rvals="rest", byref=["frame"])
        #  rs_bool pl_exp_get_oldest_frame(int16 hcam, ctypes.POINTER(ctypes.c_void_p) frame)
        self.pl_exp_get_oldest_frame=wrapper(lib.pl_exp_get_oldest_frame)
        #  rs_bool pl_exp_get_oldest_frame_ex(int16 hcam, ctypes.POINTER(ctypes.c_void_p) frame, ctypes.POINTER(FRAME_INFO) frame_info)
        self.pl_exp_get_oldest_frame_ex_lib=wrapper(lib.pl_exp_get_oldest_frame_ex, args=["hcam","frame_info"], rvals="rest", byref=["frame"])
        #  rs_bool pl_exp_unlock_oldest_frame(int16 hcam)
        self.pl_exp_unlock_oldest_frame=wrapper(lib.pl_exp_unlock_oldest_frame)

        #  rs_bool pl_cam_register_callback_ex3(int16 hcam, int32 callback_event, ctypes.c_void_p callback, ctypes.c_void_p context)
        self.pl_cam_register_callback_ex3_lib=wrapper(lib.pl_cam_register_callback_ex3)
        #  rs_bool pl_cam_deregister_callback(int16 hcam, int32 callback_event)
        self.pl_cam_deregister_callback=wrapper(lib.pl_cam_deregister_callback)
        # typedef void (PV_DECL *PL_CALLBACK_SIG_EX3)(const FRAME_INFO* pFrameInfo, void* pContext);
        self.c_callback=ctypes.WINFUNCTYPE(None,pvcam_defs.PFRAME_INFO,ctypes.c_void_p)

        #  rs_bool pl_pp_reset(int16 hcam)
        self.pl_pp_reset=wrapper(lib.pl_pp_reset)

        return

        # #  rs_bool pl_io_script_control(int16 hcam, uns16 addr, flt64 state, uns32 location)
        # self.pl_io_script_control=wrapper(lib.pl_io_script_control)
        # #  rs_bool pl_io_clear_script_control(int16 hcam)
        # self.pl_io_clear_script_control=wrapper(lib.pl_io_clear_script_control)
        # #  rs_bool pl_md_frame_decode(ctypes.POINTER(md_frame) pDstFrame, ctypes.c_void_p pSrcBuf, uns32 srcBufSize)
        # self.pl_md_frame_decode=wrapper(lib.pl_md_frame_decode)
        # #  rs_bool pl_md_frame_recompose(ctypes.c_void_p pDstBuf, uns16 offX, uns16 offY, uns16 dstWidth, uns16 dstHeight, ctypes.POINTER(md_frame) pSrcFrame)
        # self.pl_md_frame_recompose=wrapper(lib.pl_md_frame_recompose)
        # #  rs_bool pl_md_create_frame_struct_cont(ctypes.POINTER(ctypes.POINTER(md_frame)) pFrame, uns16 roiCount)
        # self.pl_md_create_frame_struct_cont=wrapper(lib.pl_md_create_frame_struct_cont)
        # #  rs_bool pl_md_create_frame_struct(ctypes.POINTER(ctypes.POINTER(md_frame)) pFrame, ctypes.c_void_p pSrcBuf, uns32 srcBufSize)
        # self.pl_md_create_frame_struct=wrapper(lib.pl_md_create_frame_struct)
        # #  rs_bool pl_md_release_frame_struct(ctypes.POINTER(md_frame) pFrame)
        # self.pl_md_release_frame_struct=wrapper(lib.pl_md_release_frame_struct)
        # #  rs_bool pl_md_read_extended(ctypes.POINTER(md_ext_item_collection) pOutput, ctypes.c_void_p pExtMdPtr, uns32 extMdSize)
        # self.pl_md_read_extended=wrapper(lib.pl_md_read_extended)


    def get_enum_value(self, hcam, param_id, index):
        l=self.pl_enum_str_length(hcam,param_id,index)
        s=ctypes.create_string_buffer(l+1)
        iv=self.pl_get_enum_param(hcam,param_id,index,ctypes.addressof(s),l)
        return iv,s.value

    numeric_params=[PARAM_TYPE.TYPE_INT8, PARAM_TYPE.TYPE_INT16, PARAM_TYPE.TYPE_INT32, PARAM_TYPE.TYPE_INT64,
                    PARAM_TYPE.TYPE_UNS8, PARAM_TYPE.TYPE_UNS16, PARAM_TYPE.TYPE_UNS32, PARAM_TYPE.TYPE_UNS64,
                    PARAM_TYPE.TYPE_FLT32, PARAM_TYPE.TYPE_FLT64, PARAM_TYPE.TYPE_BOOLEAN, PARAM_TYPE.TYPE_ENUM]
    supported_params=numeric_params+[PARAM_TYPE.TYPE_CHAR_PTR]
    def build_arg(self, typ, v=0):
        if typ==PARAM_TYPE.TYPE_INT8:
            return pvcam_defs.int8(int(v))
        if typ==PARAM_TYPE.TYPE_INT16:
            return pvcam_defs.int16(int(v))
        if typ==PARAM_TYPE.TYPE_INT32:
            return pvcam_defs.int32(int(v))
        if typ==PARAM_TYPE.TYPE_INT64:
            return pvcam_defs.long64(int(v))
        if typ==PARAM_TYPE.TYPE_UNS8:
            return pvcam_defs.uns8(int(v))
        if typ==PARAM_TYPE.TYPE_UNS16:
            return pvcam_defs.uns16(int(v))
        if typ==PARAM_TYPE.TYPE_UNS32:
            return pvcam_defs.uns32(int(v))
        if typ==PARAM_TYPE.TYPE_UNS64:
            return pvcam_defs.ulong64(int(v))
        if typ==PARAM_TYPE.TYPE_FLT32:
            return pvcam_defs.flt32(float(v))
        if typ==PARAM_TYPE.TYPE_FLT64:
            return pvcam_defs.flt64(float(v))
        if typ==PARAM_TYPE.TYPE_BOOLEAN:
            return pvcam_defs.rs_bool(bool(v))
        if typ==PARAM_TYPE.TYPE_ENUM:
            return pvcam_defs.int32(int(v))
        raise PvcamLibError("can not create parameter with type {}".format(typ))

    def get_param(self, hcam, param_id, param_attribute=0, typ=None):
        if typ is None:
            typ=self.get_param(hcam,param_id,PL_PARAM_ATTRIBUTES.ATTR_TYPE,PARAM_TYPE.TYPE_UNS16)
        if typ==PARAM_TYPE.TYPE_CHAR_PTR:
            l=self.get_param(hcam,param_id,PL_PARAM_ATTRIBUTES.ATTR_COUNT,PARAM_TYPE.TYPE_UNS32)
            s=ctypes.create_string_buffer(l)
            self.pl_get_param(hcam,param_id,param_attribute,s)    
            return py3.as_str(s.value)
        value=self.build_arg(typ)
        self.pl_get_param(hcam,param_id,param_attribute,ctypes.pointer(value))
        return value.value
    def set_param(self, hcam, param_id, value, typ=None):
        if typ is None:
            typ=self.get_param(hcam,param_id,PL_PARAM_ATTRIBUTES.ATTR_TYPE,PARAM_TYPE.TYPE_UNS16)
        value=self.build_arg(typ,value)
        self.pl_set_param(hcam,param_id,ctypes.pointer(value))

    def pl_exp_setup_seq(self, hcam, exp_total, rgns, exp_mode, exposure_time):
        rgn_total=len(rgns)
        rgn_array=(pvcam_defs.rgn_type*rgn_total)()
        for i,r in enumerate(rgns):
            rgn_array[i]=pvcam_defs.Crgn_type.prep_struct_args(*r)
        return self.pl_exp_setup_seq_lib(hcam,exp_total,rgn_total,ctypes.cast(rgn_array,pvcam_defs.rgn_ptr),exp_mode,exposure_time)
    def pl_exp_setup_cont(self, hcam, rgns, exp_mode, exposure_time, buffer_mode):
        rgn_total=len(rgns)
        rgn_array=(pvcam_defs.rgn_type*rgn_total)()
        for i,r in enumerate(rgns):
            rgn_array[i]=pvcam_defs.Crgn_type.prep_struct_args(*r)
        return self.pl_exp_setup_cont_lib(hcam,rgn_total,ctypes.cast(rgn_array,pvcam_defs.rgn_ptr),exp_mode,exposure_time,buffer_mode)
    
    def pl_exp_check_cont_status_ex(self, hcam):
        fis=self.pl_create_frame_info_struct()
        status,byte_cnt,buffer_cnt=self.pl_exp_check_cont_status_ex_lib(hcam,fis)
        fi=CFRAME_INFO.tup_struct(fis.contents)
        self.pl_release_frame_info_struct(fis)
        return status,byte_cnt,buffer_cnt,fi
    def pl_exp_get_latest_frame_ex(self, hcam):
        fis=self.pl_create_frame_info_struct()
        frame=self.pl_exp_get_latest_frame_ex_lib(hcam,fis)
        fi=CFRAME_INFO.tup_struct(fis.contents)
        self.pl_release_frame_info_struct(fis)
        return frame,fi
    def pl_exp_get_oldest_frame_ex(self, hcam):
        fis=self.pl_create_frame_info_struct()
        frame=self.pl_exp_get_oldest_frame_ex_lib(hcam,fis)
        fi=CFRAME_INFO.tup_struct(fis.contents)
        self.pl_release_frame_info_struct(fis)
        return frame,fi
    
    def pl_cam_register_callback_ex3(self, hcam, callback_event, callback, context=None, wrap=True):
        if wrap:
            def wrapped_callback(*args):
                try:
                    callback(*args)
                except: # pylint: disable=bare-except
                    pass
            cb=self.c_callback(wrapped_callback)
        else:
            cb=self.c_callback(callback)
        self.pl_cam_register_callback_ex3_lib(hcam,callback_event,cb,context)
        return cb
    
wlib=PvcamLib()