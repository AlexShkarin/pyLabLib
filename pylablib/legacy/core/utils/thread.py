"""
Simple threading routines.

A more extensive threading library is contained in the core.mthread package.
"""

import threading
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


class PeriodicThread(object):
    """
    A thread that runs in an infinite loop (until externally stopped) and executes its task with a given periodicity.

    To use, it needs to be inherited, with the subclass redefining :meth:`execute` or :meth:`process_message` method.
    """
    def __init__(self):
        object.__init__(self)
        self.running=False
        self.paused=False
        self.message_queue=Queue(1)
        self.ack_queue=Queue(1)
    
    def execute(self):
        """
        Perform a single iteration of the loop.

        To be overridden in subclasses.
        """
        pass
    def process_message(self, msg):
        """
        Process a message sent from the parent thread.

        To be overridden in subclasses.
        """
        pass
        
    def loop(self, period, sync):
        """
        Main loop methods. Called automatically in a new thread when :meth:`start` is invoked.
        """
        self.running=True
        if sync:
            self.ack_queue.put("start")
        try:
            while True:
                try:
                    msg,sync=self.message_queue.get(timeout=period if not self.paused else None)
                    if sync:
                        self.ack_queue.put(msg)
                except Empty:
                    msg=None
                if msg=="pause":
                    self.paused=True
                elif msg=="resume":
                    self.paused=False
                elif msg=="stop":
                    break
                elif msg is not None:
                    self.process_message(msg)
                if not self.paused:
                    self.execute()
        finally:
            self.running=False
            self.paused=False
        
    def wait_for_execution(self):
        """Synchronize with the thread (wait until the current iteration is executed)."""
        self.send_message(None,sync=True)
    def send_message(self, msg, sync=True):
        """
        Send a message to the thread.
        
        The message is processed by the thread in the :meth:`process_message` method (by default does nothing).
        If ``sync==True``, wait until the thread received (not necessarily processed) the message.
        """
        if self.running:
            self.message_queue.put((msg,sync))
            if sync:
                ack_msg=self.ack_queue.get()
                if ack_msg!=msg:
                    raise RuntimeError("wrong acknowledgment '{0}' for message '{1}'".format(ack_msg,msg))
        else:
            raise RuntimeError("thread is not running")
    def start(self, period, sync=True):
        """
        Start the thread.

        `period` specifies the job execution period, in seconds.
        If ``sync==True``, wait until the thread is started.
        """
        if self.running:
            raise RuntimeError("thread is already running")
        threading.Thread(target=self.loop,args=(period,sync)).start()
        if sync:
            ack_msg=self.ack_queue.get()
            if ack_msg!="start":
                raise RuntimeError("wrong acknowledgment '{0}' for message 'start'".format(ack_msg))
    def stop(self, sync=True):
        """
        Stop the thread.

        If ``sync==True``, wait until the thread is stopped.
        """
        self.send_message("stop",sync=sync)
    def pause(self, sync=True):
        """
        Pause the thread execution.

        If ``sync==True``, wait until the thread is paused.
        """
        self.send_message("pause",sync=sync)
    def resume(self, sync=True):
        """
        Resume the thread execution.

        If ``sync==True``, wait until the thread is resumed.
        """
        self.send_message("resume",sync=sync)
    
    def is_looping(self):
        """Check if the thread is actively executing (not paused)."""
        return self.running and not self.paused
    def is_running(self):
        """Check if the thread is running (possibly paused)."""
        return self.running