from . import controller, threadprop
import time

try:
    import yappi
except ImportError:
    yappi=None



def _check_yappi():
    if yappi is None:
        msg=(   "operation requires yappi library. You can install it via PyPi as 'pip install yappi'. "
                "If it is installed, check if it imports correctly by running 'import yappi'")
        raise ImportError(msg)


_wall_timer=time.time()
def start(reset=True):  # pylint: disable=redefined-outer-name
    """
    Start yappi profile logging.
    
    If ``reset==True``, reset the stats.
    """
    _check_yappi()
    global _wall_timer  # pylint: disable=global-statement
    yappi.set_clock_type("cpu")
    yappi.stop()
    if reset:
        yappi.clear_stats()
        _wall_timer=time.time()
    yappi.start()
def reset():
    """Reset yappi profiling stats"""
    _check_yappi()
    global _wall_timer  # pylint: disable=global-statement
    yappi.clear_stats()
    _wall_timer=time.time()
def stop():
    """Stop yappi profiling"""
    _check_yappi()
    yappi.stop()
def get_stats():
    """
    Get yappi profiling stats.

    Return tuple ``((ttime,wtime), (threads,ctls))``.
    Here ``ttime`` and ``wtime`` are total execution time (sum of all thread times) and the wall time (since the last reset) respectively.
    ``threads`` are yappi-generated stats, and ``ctls`` is the list ``[(name,ctl)]`` with the controller names and thread controllers,
    which are ordered in the same way as ``threads`` (for any non-controlled or stopped thread these are set to ``None``).
    """
    _check_yappi()
    threads=yappi.get_thread_stats()
    ttime=sum(th.ttot for th in threads)
    wtime=time.time()-_wall_timer
    ctls=[]
    for th in threads:
        try:
            ctl=controller.get_controller(th.tid,sync=False)
            ctl_name=ctl.name
        except threadprop.NoControllerThreadError:
            ctl=None
            ctl_name=None
        ctls.append((ctl_name,ctl))
    return (ttime,wtime),(threads,ctls)
def print_stats(nfunc=None, ntotfunc=None, min_func_frac=.001):
    """
    Print yappi profiling stats.

    `nfunc` is the number of top (most expensive) functions to print per each thread,
    `ntotfunc` is the number of global top function to print; ``None`` for either means that they are not printed.
    `min_func_frac` specifies the minimal fraction of the total time for which the function stats are still printed
    (to prevent lost of printouts for "cheap" threads).
    """
    (ttime,wtime),(threads,ctls)=get_stats()
    print("{:60s}  {:8.3f}s".format("WALL",wtime))
    print("{:60s}  {:8.3f}s     {:6.1f}%".format("TOTAL",ttime,ttime/wtime*100))
    if ntotfunc is not None:
        funcstat=yappi.get_func_stats()
        for f in funcstat[:ntotfunc]:
            if f.ttot>=min_func_frac*ttime:
                print(" "*4+"{:50s} {:5d}  {:8.3f}s        {:.1f}%".format(f.name,f.ncall,f.ttot,f.ttot/ttime*100))
    for th,(ctl_name,_) in zip(threads,ctls):
        print("{:60s}  {:8.3f}s    {:6.1f}%   {:5d}".format(ctl_name or "[unknown]",th.ttot,th.ttot/ttime*100,th.sched_count))
        if nfunc is not None:
            funcstat=yappi.get_func_stats(ctx_id=th.id)
            for f in funcstat[:nfunc]:
                if f.ttot>min_func_frac*ttime:
                    print(" "*4+"{:50s} {:5d}  {:8.3f}s        {:6.1f}% / {:6.1f}%".format(f.name,f.ncall,f.ttot,f.ttot/th.ttot*100,f.ttot/ttime*100))