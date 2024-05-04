import cython
from libc.string cimport memcpy

ctypedef long long int int64_t
ctypedef unsigned int DWORD

ctypedef int64_t (*pFg_getStatusEx)(void *Fg, int Param, int64_t Data, unsigned DmaIndex, void *pMem) nogil
ctypedef int (*pFg_AcquireEx)(void *Fg, unsigned DmaIndex, int64_t PicCount, int nFlag, void *pMem) noexcept nogil
cdef extern void Sleep(DWORD dwMilliseconds) nogil

cdef enum:
    ACQ_STANDARD=1
    NUMBER_OF_GRABBED_IMAGES=10
cdef enum:
    acq_overflow_period=(1<<24L)
    acq_neg_allowed=(1<<20L)

# @cython.cdivision(True)
# cdef int64_t clooper(void *Fg, unsigned port, void *pMem, char *src, char *dst, size_t frame_size, size_t src_nframes, size_t dst_nframes, int64_t run_nframes,
#             unsigned *looping, int64_t *nread, int64_t *oldest_valid, int64_t *debug_info, pFg_getStatusEx Fg_getStatusEx, pFg_AcquireEx Fg_AcquireEx) nogil:
#     cdef int64_t nacq=0, prev_nacq=0, new_nacq
#     cdef size_t i, ncpy
#     cdef int src_ovf
#     cdef int to_cnt=0
#     cdef int64_t local_debug_info[3]
#     if not debug_info:
#         debug_info=local_debug_info
#     if Fg_AcquireEx:
#         Fg_AcquireEx(Fg,port,run_nframes,ACQ_STANDARD,pMem)
#     debug_info[1]=0
#     debug_info[2]=0
#     while looping[0]:
#         debug_info[1]+=1
#         new_nacq=Fg_getStatusEx(Fg,NUMBER_OF_GRABBED_IMAGES,0,port,pMem)
#         debug_info[0]=new_nacq
#         if new_nacq==-2120:  # FG_TIMEOUT_ERR
#             to_cnt+=1
#             if to_cnt<60E3:
#                 Sleep(1)
#                 continue
#         if new_nacq<0:
#             return new_nacq
#         to_cnt=0
#         nacq+=(new_nacq-prev_nacq+acq_neg_allowed)%acq_overflow_period-acq_neg_allowed
#         prev_nacq=new_nacq
#         if nacq<=nread[0]:
#             # Sleep(1)
#             continue
#         debug_info[2]+=1
#         ncpy=nacq-nread[0]
#         src_ovf=ncpy>src_nframes
#         ncpy=min(ncpy,src_nframes,dst_nframes)
#         for i in range(nacq-ncpy,nacq):
#             memcpy(dst+(i%dst_nframes)*frame_size,src+(i%src_nframes)*frame_size,frame_size)
#         nread[0]=nacq
#         if src_ovf:
#             oldest_valid[0]=nacq-ncpy
#     return 0

# def looper(size_t Fg, unsigned port, size_t pMem, size_t src, size_t dst, size_t frame_size, size_t src_nframes, size_t dst_nframes, int64_t run_nframes,
#                 size_t looping, size_t nread, size_t oldest_valid, size_t debug_info, size_t Fg_getStatusEx, size_t Fg_AcquireEx):
#     cdef int64_t result=0
#     with nogil:
#         result=clooper(<void*>Fg,port,<void*>pMem,<char*>src,<char*>dst,frame_size,src_nframes,dst_nframes,run_nframes,
#                     <unsigned*>looping,<int64_t*>nread,<int64_t*>oldest_valid,<int64_t*>debug_info,<pFg_getStatusEx>Fg_getStatusEx,<pFg_AcquireEx>Fg_AcquireEx)
#     return result

@cython.cdivision(True)
cdef int64_t clooper(void *Fg, unsigned port, void *pMem, char *src, char *dst, size_t frame_size, size_t src_nframes, size_t dst_nframes, int64_t run_nframes,
            unsigned *looping, int64_t *new_nacq, int64_t *nread, int64_t *oldest_valid, int64_t *debug_info,
            pFg_getStatusEx Fg_getStatusEx, pFg_AcquireEx Fg_AcquireEx) nogil:
    cdef int64_t nacq=0, prev_nacq=0, curr_nacq
    cdef int64_t nstart, sstart, dstart, nchunk
    cdef size_t i, ncpy
    cdef int src_ovf
    cdef int to_cnt=0
    cdef int64_t local_debug_info[3]
    if not debug_info:
        debug_info=local_debug_info
    if Fg_AcquireEx:
        Fg_AcquireEx(Fg,port,run_nframes,ACQ_STANDARD,pMem)
    debug_info[1]=0
    debug_info[2]=0
    while looping[0]:
        curr_nacq=new_nacq[0]
        debug_info[0]=curr_nacq
        debug_info[1]+=1
        if curr_nacq<0:
            return curr_nacq
        to_cnt=0
        nacq+=(curr_nacq-prev_nacq+acq_neg_allowed)%acq_overflow_period-acq_neg_allowed
        prev_nacq=curr_nacq
        if nacq<=nread[0]:
            continue
        debug_info[2]+=1
        ncpy=nacq-nread[0]
        src_ovf=ncpy>src_nframes
        ncpy=min(ncpy,src_nframes,dst_nframes)
        # for i in range(nacq-ncpy,nacq):
        #     memcpy(dst+(i%dst_nframes)*frame_size,src+(i%src_nframes)*frame_size,frame_size)
        nstart=nacq-ncpy
        while nstart<nacq:
            sstart=nstart%src_nframes
            dstart=nstart%dst_nframes
            nchunk=min(nacq-nstart,src_nframes-sstart,dst_nframes-dstart)
            memcpy(dst+dstart*frame_size,src+sstart*frame_size,nchunk*frame_size)
            nstart+=nchunk
        nread[0]=nacq
        if src_ovf:
            oldest_valid[0]=nacq-ncpy
    return 0

def looper(size_t Fg, unsigned port, size_t pMem, size_t src, size_t dst, size_t frame_size, size_t src_nframes, size_t dst_nframes, int64_t run_nframes,
                size_t looping, size_t new_nacq, size_t nread, size_t oldest_valid, size_t debug_info, size_t Fg_getStatusEx, size_t Fg_AcquireEx):
    cdef int64_t result=0
    with nogil:
        result=clooper(<void*>Fg,port,<void*>pMem,<char*>src,<char*>dst,frame_size,src_nframes,dst_nframes,run_nframes,
                    <unsigned*>looping,<int64_t*>new_nacq,<int64_t*>nread,<int64_t*>oldest_valid,<int64_t*>debug_info,
                    <pFg_getStatusEx>Fg_getStatusEx,<pFg_AcquireEx>Fg_AcquireEx)
    return result



cdef int ccallback(int64_t frame, int64_t *data):
    if data[0]<frame:
        data[0]=frame
    return 0
def get_callback():
    return <size_t>(&ccallback)