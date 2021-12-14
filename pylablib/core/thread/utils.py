import threading
import contextlib


class ReadChangeLock:
    """
    Lock based on condition variables which handles a state which can be read or changed.

    Any number of threads can read simultaneously, but changing is incompatible with other reading or changing.
    """
    def __init__(self):
        self.cv=threading.Condition(threading.RLock())
        self.state=0
    def can_read(self):
        """Check if the state can be read"""
        return self.state>=0
    def can_change(self):
        """Check if the state can be changed"""
        return self.state==0
    @contextlib.contextmanager
    def reading(self):
        """Context manager denoting reading event"""
        with self.cv:
            self.cv.wait_for(self.can_read)
            self.state+=1
        try:
            yield
        finally:
            with self.cv:
                self.state-=1
                self.cv.notify()
    @contextlib.contextmanager
    def changing(self):
        """Context manager denoting changing event"""
        with self.cv:
            self.cv.wait_for(self.can_change)
            self.state=-1
        try:
            yield
        finally:
            with self.cv:
                self.state=0
                self.cv.notify_all()