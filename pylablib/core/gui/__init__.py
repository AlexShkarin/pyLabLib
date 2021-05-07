qt_present=False
is_pyqt5=False
iq_pyside2=False

try:
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
    from sip import delete as qdelete
    qt_present=is_pyqt5=True
except ImportError:
    try:
        from PySide2 import QtGui, QtWidgets, QtCore
        from PySide2.QtCore import Signal, Slot
        from shiboken2 import delete as qdelete
        qt_present=iq_pyside2=True
    except ImportError:
        pass

if qt_present:
    from . import value_handling
    from .value_handling import GUIValues

    from . import formatter
    from .formatter import FloatFormatter, IntegerFormatter, FmtStringFormatter, as_formatter

    from . import limiter
    from .limiter import NumberLimit, as_limiter

    from . import utils as gui_utils