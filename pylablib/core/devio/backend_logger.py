from ..utils import string, py3

import contextlib

class BackendLogger:
    """
    Backend logger.

    Receives log requests from backends and stores them in a predefined file.

    Args:
        path: path to save the log
    """
    def __init__(self, path):
        self.path=path
        self.started=False
        self.file=None
    def start(self, header):
        """Start logging section"""
        self.file=open(self.path,"a" if self.started else "w")
        self.file.write("h {}".format(header)+"\n")
        self.started=True
    def stop(self):
        """Stop logging section"""
        self.file.close()
        self.file=None
    @contextlib.contextmanager
    def section(self, header):
        """Context manager for operations within a header"""
        self.start(header)
        try:
            yield
        finally:
            self.stop()
    def log(self, operation, value):
        """Log the operation"""
        if self.file is not None:
            value=string.escape_string(py3.as_str(value),location="entry")
            if operation=="read":
                self.file.write("r "+value+"\n")
            elif operation=="write":
                self.file.write("w "+value+"\n")
            elif operation=="error":
                self.file.write("e "+value+"\n")
            else:
                raise ValueError("unrecognized operation: {}".format(operation))


def load_logfile(path):
    """
    Load backend log file.
    
    Return a list of tuples ``[(header, section)]``, where ``header`` is the header name,
    and ``section`` is the list ``[(op, value)]`` with operations (``"r"``, ``"w"``, or ``"e"``)
    nd corresponding values.
    """
    with open(path,"r") as f:
        lines=[ln.strip() for ln in f.readlines() if ln.strip()]
    sections=[]
    csec=(None,[])
    for ln in lines:
        if ln[0]=="h":
            if csec[0]:
                sections.append(csec)
            csec=(ln[2:],[])
        elif ln[0] in "erw":
            if not csec[0]:
                raise IOError("operation {} is outside a header".format(ln))
            csec[1].append((ln[0],string.unescape_string(ln[2:])))
        else:
            raise IOError("unrecognized entry line: {}".format(ln))
    if csec[0]:
        sections.append(csec)
    return sections