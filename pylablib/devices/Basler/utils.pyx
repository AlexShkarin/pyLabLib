import cython
from libc.stdlib cimport malloc, free

from . import pylonC_defs
import ctypes

cdef int ret_val_size=ctypes.sizeof(pylonC_defs.PylonGrabResult_t)

ctypedef int (*pPylonStreamGrabberRetrieveResult)(void *hStg, void *pGrabResult, unsigned char *pReady) noexcept nogil
ctypedef int (*pPylonStreamGrabberQueueBuffer)(void *hStg, void *hBuf, void *pContext) noexcept nogil
ctypedef int (*pPylonWaitObjectWait)(void *hWobj, unsigned timeout, void *pResult) noexcept nogil


@cython.cdivision(True)
cdef int clooper(void *strm, void *wtobj, unsigned nbuff, void **hbuffers, int *looping, unsigned *nread,
            pPylonStreamGrabberRetrieveResult PylonStreamGrabberRetrieveResult, pPylonStreamGrabberQueueBuffer PylonStreamGrabberQueueBuffer, pPylonWaitObjectWait PylonWaitObjectWait) nogil:
    cdef int code=0
    cdef unsigned char ret_rdy=0
    cdef void *ret_vals=malloc(ret_val_size)
    while (not code) and looping[0]:
        ret_rdy=0
        code=PylonWaitObjectWait(wtobj,10,&ret_rdy)
        if code:
            break
        if not ret_rdy:
            continue
        code=PylonStreamGrabberRetrieveResult(strm,ret_vals,&ret_rdy)
        if code:
            break
        if not ret_rdy:
            continue
        PylonStreamGrabberQueueBuffer(strm,hbuffers[nread[0]%nbuff],NULL)
        nread[0]+=1
    free(ret_vals)
    return code

def looper(size_t strm, size_t wtobj, unsigned nbuff, size_t hbuffers, size_t looping, size_t nread,
                    size_t PylonStreamGrabberRetrieveResult, size_t PylonStreamGrabberQueueBuffer, size_t PylonWaitObjectWait):
    cdef int result=0
    with nogil:
        result=clooper(<void *>strm,<void *>wtobj,nbuff,<void **>hbuffers,<int *>looping,<unsigned *>nread,
                    <pPylonStreamGrabberRetrieveResult>PylonStreamGrabberRetrieveResult,<pPylonStreamGrabberQueueBuffer>PylonStreamGrabberQueueBuffer,<pPylonWaitObjectWait>PylonWaitObjectWait)
    return result