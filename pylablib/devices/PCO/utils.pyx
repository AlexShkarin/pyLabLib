import cython
from libc.stdlib cimport malloc, free

ctypedef void *HANDLE
ctypedef int BOOL
ctypedef char *LPCSTR
ctypedef unsigned short WORD
ctypedef unsigned int DWORD

cdef extern HANDLE CreateEventA(void *lpEventAttributes, BOOL bManualReset, BOOL bInitialState, LPCSTR lpName) nogil
cdef extern BOOL CloseHandle(HANDLE hObject) nogil
cdef extern BOOL ResetEvent(HANDLE hEvent) nogil
cdef extern DWORD WaitForSingleObject(HANDLE hHandle, DWORD dwMilliseconds) nogil
cdef extern void Sleep(DWORD dwMilliseconds) nogil

ctypedef int (*pPCO_AddBufferExtern)(HANDLE ph, HANDLE hEvent, WORD wActSeg, DWORD dw1stImage, DWORD dwLastImage, DWORD dwSynch, void *pBuf, DWORD dwLen, DWORD *dwStatus) noexcept nogil
ctypedef int (*pNotify)()

cdef DWORD max_sched_buff=32

@cython.cdivision(True)
cdef int clooper(HANDLE hcam, DWORD nbuff, void **buffers, DWORD buffer_size, int set_idx,
                    int *looping, DWORD *nscheduled, DWORD *nread, pNotify Notify, pPCO_AddBufferExtern PCO_AddBufferExtern) nogil:
    nbuff=max(nbuff,1U)
    cdef DWORD tosched=min(nbuff,max_sched_buff)
    cdef HANDLE *events=<HANDLE*>malloc(nbuff*sizeof(HANDLE))
    cdef DWORD *statuses=<DWORD*>malloc(nbuff*sizeof(DWORD))
    cdef DWORD i, ib
    for i in range(nbuff):
        events[i]=CreateEventA(NULL,True,False,NULL)
        statuses[i]=0
    cdef int code=0
    for i in range(tosched):
        ib=i+1 if set_idx else 0
        code=PCO_AddBufferExtern(hcam,events[i],0,ib,ib,0,buffers[i],buffer_size,statuses+i)
        nscheduled[0]+=1
        if code:
            break
    if Notify:
        with gil:
            Notify()
    cdef int acted
    while (not code) and looping[0]:
        acted=False
        if nread[0]<nscheduled[0]:
            ib=nread[0]%nbuff
            if WaitForSingleObject(events[ib],1)==0:
                nread[0]+=1
                acted=True
        if nscheduled[0]<nread[0]+tosched:
            ib=nscheduled[0]%nbuff
            ResetEvent(events[ib])
            code=PCO_AddBufferExtern(hcam,events[ib],0,0,0,0,buffers[ib],buffer_size,statuses+ib)
            nscheduled[0]+=1
            acted=True
        if not acted:
            Sleep(1)
    for i in range(nbuff):
        CloseHandle(events[i])
    free(events)
    free(statuses)
    return code


def looper(size_t hcam, DWORD nbuff, size_t buffers, DWORD buffer_size, int set_idx,
                    size_t looping, size_t nscheduled, size_t nread, size_t Notify, size_t PCO_AddBufferExtern):
    cdef int result=0
    with nogil:
        result=clooper(<HANDLE>hcam,nbuff,<void**>buffers,buffer_size,set_idx,
                    <int*>looping,<DWORD*>nscheduled,<DWORD*>nread,<pNotify>Notify,<pPCO_AddBufferExtern>PCO_AddBufferExtern)
    return result