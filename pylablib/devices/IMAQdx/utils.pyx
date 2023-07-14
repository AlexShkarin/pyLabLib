cdef unsigned imaqdx_frame_callback(unsigned sid, unsigned bidx, void *data):
    cdef unsigned *comm=<unsigned*>(data)
    cdef unsigned *stat=<unsigned*>(data)+1
    if comm[0]:
        stat[0]=bidx+1
        return 1
    return 0
def get_callback():
    return <size_t>(&imaqdx_frame_callback)