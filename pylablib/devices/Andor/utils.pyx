import cython
from libc.string cimport memcpy

ctypedef int (*pAT_WaitBuffer)(int Hndl, void **Ptr, int *PtrSize, unsigned int Timeout) noexcept nogil
ctypedef int (*pAT_QueueBuffer)(int Hndl, void *Ptr, int PtrSize) noexcept nogil

@cython.cdivision(True)
cdef int clooper(int Hndl, unsigned nbuff, void **hbuffers, int esize, int queued, int *looping, unsigned *nread,
            pAT_WaitBuffer AT_WaitBuffer, pAT_QueueBuffer AT_QueueBuffer) nogil:
    cdef int size=0
    cdef int code=0
    cdef void* buffer=<void*>(0)
    while looping[0]:
        code=AT_WaitBuffer(Hndl,&buffer,&size,300)
        if code==13 or code==11:  # AT_ERR_TIMEDOUT or AT_ERR_NODATA
            continue
        if code:
            return code
        if size!=esize:
            return -1
        AT_QueueBuffer(Hndl,hbuffers[(nread[0]+queued)%nbuff],esize)
        nread[0]+=1
    return code

def looper(int Hndl, unsigned nbuff, size_t hbuffers, int esize, int queued, size_t looping, size_t nread,
                    size_t AT_WaitBuffer, size_t AT_QueueBuffer):
    cdef int result=0
    with nogil:
        result=clooper(Hndl,nbuff,<void **>hbuffers,esize,queued,<int *>looping,<unsigned *>nread,
                    <pAT_WaitBuffer>AT_WaitBuffer,<pAT_QueueBuffer>AT_QueueBuffer)
    return result


cdef int ccopyframes(unsigned nbuff, char **hbuffers, unsigned size, unsigned start, unsigned ncpy, unsigned off, char *dst) nogil:
    cdef unsigned i=0
    for i in range(ncpy):
        memcpy(dst,hbuffers[(start+i)%nbuff]+off,size)
        dst+=size
    return 0

def copyframes(unsigned nbuff, size_t hbuffers, unsigned size, unsigned start, unsigned ncpy, unsigned off, size_t dst):
    with nogil:
        ccopyframes(nbuff,<char**>hbuffers,size,start,ncpy,off,<char*>dst)