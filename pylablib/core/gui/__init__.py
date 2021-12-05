import warnings
import collections

is_pyqt5=False
is_pyside2=False
_TQtKWArgs=collections.namedtuple("TQtKWArgs",["file_dialog_dir"])
qtkwargs=_TQtKWArgs("dir")

try:
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
    try:
        from PyQt5.sip import delete as qdelete  # pylint: disable=no-name-in-module
    except ImportError:  # PyQt5<5.11 versions require separate sip
        try:
            from sip import delete as qdelete  # pylint: disable=no-name-in-module
        except ImportError:
            warnings.warn("could not find sip required for some PyQt5 functionality; you need to either install it explicitly from PyPi, or update your PyQt5 version to 5.11 or above")
            qdelete=None
    is_pyqt5=True
    qtkwargs=_TQtKWArgs("directory")
except ImportError:
    try:
        from PySide2 import QtGui, QtWidgets, QtCore
        from PySide2.QtCore import Signal, Slot
        from shiboken2 import delete as qdelete  # pylint: disable=no-name-in-module
        is_pyside2=True
    except ImportError:
        pass

qt_present=is_pyqt5 or is_pyside2