from PyQt5 import QtWidgets, QtCore
from ... import format, limit

class LVTextEdit(QtWidgets.QLineEdit):
    """
    Expanded text edit.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    """
    def __init__(self, parent, value=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.returnPressed.connect(self._on_enter)
        self.editingFinished.connect(self._on_edit_done)
        self._value=None
        if value is not None:
            self.set_value(value)
        self.textChanged.connect(self._on_change_text)
    def _on_edit_done(self):
        self.set_value(self.text())
        self.value_entered.emit(self._value)
    def _on_enter(self):
        self._on_edit_done()
        self.clearFocus()
    def _on_change_text(self, text):
        if not self.isModified():
            self.set_value(text)
    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Escape:
            self.clearFocus()
            self.show_value()
        else:
            QtWidgets.QLineEdit.keyPressEvent(self,event)

    value_entered=QtCore.pyqtSignal("PyQt_PyObject")
    """Signal emitted when value is entered (regardless of whether it stayed the same)"""
    value_changed=QtCore.pyqtSignal("PyQt_PyObject")
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current numerical value"""
        return self._value
    def show_value(self, interrupt_edit=False):
        """
        Display currently stored numerical value
        
        If ``interrupt_edit==True`` and the edit is currently being modified by the user, don't update the display.
        """
        if (not self.hasFocus()) or interrupt_edit:
            self.setText(self._value)
    def set_value(self, value, notify_value_change=True, interrupt_edit=False):
        """
        Set current numerical value.
        
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        If ``interrupt_edit==True`` and the edit is currently being modified by the user, don't update the display (but still update the internally stored value).
        """
        value_changed=False
        value=str(value)
        if self._value!=value:
            self._value=value
            if notify_value_change:
                self.value_changed.emit(self._value)
            value_changed=True
        self.show_value(interrupt_edit=interrupt_edit)
        return value_changed

class LVNumEdit(QtWidgets.QLineEdit):
    """
    Labview-style numerical edit.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    Supports different number representations, metric perfixes (in input or output), keyboard shortcuts (up/down for changing number, escape for cancelling).
    """
    def __init__(self, parent, value=None, num_limit=None, num_format=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.num_limit=limit.as_limiter(num_limit) if num_limit is not None else limit.NumberLimit()
        self.num_format=format.as_formatter(num_format) if num_format is not None else format.FloatFormatter()
        self.returnPressed.connect(self._on_enter)
        self.editingFinished.connect(self._on_edit_done)
        self._value=None
        if value is not None:
            self.set_value(value)
        else:
            self.set_value(0)
            if self._value is None:
                raise ValueError("can't assign a safe default value")
        self.textChanged.connect(self._on_change_text)
    def _on_edit_done(self):
        self.set_value(self._read_input())
        self.value_entered.emit(self._value)
    def _on_enter(self):
        self._on_edit_done()
        self.clearFocus()
    def _on_change_text(self, text):
        if not self.isModified():
            try:
                value=format.str_to_float(str(self.text()))
                self.set_value(value)
            except ValueError:
                pass
    def keyPressEvent(self, event):
        k=event.key()
        if k==QtCore.Qt.Key_Escape:
            self.show_value(interrupt_edit=True)
            self.clearFocus()
        elif k in [QtCore.Qt.Key_Up,QtCore.Qt.Key_Down]:
            try:
                str_value=str(self.text())
                num_value=format.str_to_float(str_value)
                cursor_order=self.get_cursor_order()
                if cursor_order!=None:
                    step=10**(cursor_order)
                    if k==QtCore.Qt.Key_Up:
                        self.set_value(num_value+step,interrupt_edit=True)
                    else:
                        self.set_value(num_value-step,interrupt_edit=True)
            except ValueError:
                self.show_value(interrupt_edit=True)
        else:
            QtWidgets.QLineEdit.keyPressEvent(self,event)
    def _read_input(self):
        try:
            return format.str_to_float(str(self.text()))
        except ValueError:
            return self._value

    def change_limiter(self, limiter, new_value=None):
        """Change current numerical limiter"""
        self.num_limit=limit.as_limiter(limiter)
        if new_value is None:
            new_value=self._value
        new_value=self._coerce_value(new_value,coerce_on_limit=True)
        if new_value!=self._value:
            self.set_value(new_value)
    def set_number_limit(self, lower_limit=None, upper_limit=None, action="ignore", value_type=None):
        """
        Set number limit.
        
        `lower_limit` and `upper_limit` set the value limits (``None`` means no limit).
        `action` specifies the action on out-of-limit: either ``"ignore"`` (return to the previously stored value), or ``"coerce"`` (coerce to the closest limit)
        `value_type` can be either ``"float"`` (any floating point number is accepted), or ``"int"`` (round to the nearest integer).
        """
        limiter=limit.NumberLimit(lower_limit=lower_limit,upper_limit=upper_limit,action=action,value_type=value_type)
        self.change_limiter(limiter)
    def change_formatter(self, formatter):
        """Change current numerical formatter"""
        self.num_format=format.as_formatter(formatter)
        self.show_value()
    def set_number_format(self, kind="float", *args, **kwargs):
        """
        Set numerical format
        
        `kind` specifies the format kind (``"float"`` or ``"int"``), and the additional arguments are passed to the corresponding formatter.
        See :class:`.format.FloatFormatter` and :class:`.format.IntegerFormatter` for details.
        """
        if kind=="float":
            formatter=format.FloatFormatter(*args,**kwargs)
        elif kind=="int":
            formatter=format.IntegerFormatter()
        else:
            raise ValueError("unknown format: {}".format(kind))
        self.change_formatter(formatter)

    def get_cursor_order(self):
        """Get a decimal order of the text cursor"""
        str_value=str(self.text())
        cursor_pos=self.cursorPosition()
        return format.pos_to_order(str_value,cursor_pos)
    def set_cursor_order(self, order):
        """Move text cursor to a given decimal order"""
        if order is not None:
            new_cursor_pos=format.order_to_pos(str(self.text()),order)
            self.setCursorPosition(new_cursor_pos)

    def _coerce_value(self, value, coerce_on_limit=False):
        for _ in range(10):
            str_value=self.num_format(value)
            num_value=format.str_to_float(str_value)
            try:
                new_value=self.num_limit(num_value)
            except limit.LimitError:
                if coerce_on_limit and isinstance(self.num_limit,limit.NumberLimit):
                    if self.num_limit.range[0] is not None and num_value<self.num_limit.range[0]:
                        new_value=self.num_limit.range[0]
                    else:
                        new_value=self.num_limit.range[1]
                else:
                    raise
            if new_value==value:
                return new_value
            value=new_value
        raise ValueError("couldn't coerce the new value")
    def repr_value(self, value):
        """Return representation of `value` according to the current numerical format"""
        return self.num_format(value)

    value_entered=QtCore.pyqtSignal("PyQt_PyObject")
    """Signal emitted when value is entered (regardless of whether it stayed the same)"""
    value_changed=QtCore.pyqtSignal("PyQt_PyObject")
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current numerical value"""
        return self._value
    def show_value(self, interrupt_edit=False, preserve_cursor_order=True):
        """
        Display currently stored numerical value
        
        If ``interrupt_edit==True`` and the edit is currently being modified by the user, don't update the display.
        If ``preserve_cursor_order==True`` and the display value is being edited, keep the decimal order of the cursor position after change.
        """
        if (not self.hasFocus()) or interrupt_edit:
            if preserve_cursor_order and self.hasFocus():
                cursor_order=self.get_cursor_order()
                self.setText(self.num_format(self._value))
                if cursor_order is not None:
                    self.set_cursor_order(cursor_order)
            else:
                self.setText(self.num_format(self._value))
    def set_value(self, value, notify_value_change=True, interrupt_edit=False, preserve_cursor_order=True):
        """
        Set and display current numerical value.
        
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        If ``interrupt_edit==True`` and the edit is currently being modified by the user, don't update the display (but still update the internally stored value).
        If ``preserve_cursor_order==True`` and the display value is being edited, keep the decimal order of the cursor position after change.
        """
        value_changed=False
        try:
            value=self._coerce_value(value)
            if self._value!=value:
                self._value=value
                if notify_value_change:
                    self.value_changed.emit(self._value)
                value_changed=True
        except limit.LimitError:
            pass
        self.show_value(interrupt_edit=interrupt_edit,preserve_cursor_order=preserve_cursor_order)
        return value_changed