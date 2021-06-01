is_pyqt5=False
is_pyside2=False

try:
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
    from sip import delete as qdelete
    is_pyqt5=True
except ImportError:
    try:
        from PySide2 import QtGui, QtWidgets, QtCore
        from PySide2.QtCore import Signal, Slot
        from shiboken2 import delete as qdelete
        is_pyside2=True
    except ImportError:
        pass

qt_present=is_pyqt5 or is_pyside2