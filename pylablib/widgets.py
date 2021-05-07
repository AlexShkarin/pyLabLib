from .core.gui import qt_present
if qt_present:
    from .core.gui.widgets import *
    from .gui.widgets import *