from .. import QtCore, QtWidgets, Signal, utils

from ..limiter import as_limiter, LimitError, NumberLimit
from ..formatter import as_formatter, str_to_float, order_to_pos, pos_to_order

class TextEdit(QtWidgets.QLineEdit):
    """
    Expanded text edit.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    """
    def __init__(self, parent, value=None):
        super().__init__(parent)
        self.returnPressed.connect(self._on_enter)
        self.editingFinished.connect(self._on_edit_done)
        self._value=None
        if value is not None:
            self.set_value(value)
        self.textChanged.connect(self._on_change_text)
        self._expand_border=None
        self._exp_parameters=None
        self._exp_placeholder=None
        self._exp_frame=None
        self._expanded=False
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
            super().keyPressEvent(event)

    def set_expandable(self, left=0, right=0, top=0, bottom=0):
        """
        Make text edit expandable.

        If it is expandable, the edit size is expanded by the given size into the corresponding directions.
        If all are zero, the widget behaves as normal.
        """
        if any([left,right,top,bottom]):
            self._expand_border=(left,right,top,bottom)
        else:
            self._expand_border=None
    def _make_exp_frame(self, pos, size, border):
        frame=QtWidgets.QFrame(utils.get_top_parent(self))
        frame.setLayout(QtWidgets.QVBoxLayout())
        pad=4
        frame.layout().setContentsMargins(pad,pad,pad,pad)
        pos=frame.parentWidget().mapFromGlobal(pos)
        frame.move(pos.x()-border[0]-pad,pos.y()-border[2]-pad)
        frame.setFixedWidth(size.width()+border[0]+border[1]+pad*2)
        frame.setFixedHeight(size.height()+border[2]+border[3]+pad*2)
        return frame
    def focusInEvent(self, evt):
        if self._expand_border is not None and self._exp_placeholder is None:
            loc=utils.get_widget_location(self)
            size_rng=self.minimumWidth(),self.maximumWidth(),self.minimumHeight(),self.maximumHeight()
            self._exp_parameters=loc,size_rng
            parent=self.parentWidget()
            pos,size=parent.mapToGlobal(self.pos()),self.size()
            parent.setUpdatesEnabled(False)
            self._exp_placeholder=QtWidgets.QWidget(parent)
            self._exp_placeholder.setFixedWidth(self.width())
            self._exp_placeholder.setFixedHeight(self.height())
            if loc is not None:
                utils.place_widget_at_location(self._exp_placeholder,loc)
                loc.layout.removeWidget(self)
            self._exp_frame=self._make_exp_frame(pos,size,self._expand_border)
            self._exp_frame.layout().addWidget(self)
            self._exp_frame.setVisible(True)
            self.setFocus()
            parent.setUpdatesEnabled(True)
            self._expanded=True
        return super().focusInEvent(evt)
    def focusOutEvent(self, evt):
        if self._expanded:
            self._expanded=False
            loc,size_rng=self._exp_parameters
            self.setMinimumWidth(size_rng[0])
            self.setMaximumWidth(size_rng[1])
            self.setMinimumHeight(size_rng[2])
            self.setMaximumHeight(size_rng[3])
            self._exp_frame.layout().removeWidget(self)
            utils.place_widget_at_location(self,loc)
            self._exp_frame.hide()
            utils.delete_widget(self._exp_placeholder)
            utils.delete_widget(self._exp_frame)
            self._exp_parameters=None
            self._exp_placeholder=None
            self._exp_frame=None
        return super().focusOutEvent(evt)
    
    value_entered=Signal(object)
    """Signal emitted when value is entered (regardless of whether it stayed the same)"""
    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current text value"""
        return self._value
    def show_value(self, interrupt_edit=False):
        """
        Display currently stored text value
        
        If ``interrupt_edit==True`` and the edit is currently being modified by the user, don't update the display.
        """
        if (not self.hasFocus()) or interrupt_edit:
            self.setText(self._value)
    def set_value(self, value, notify_value_change=True, interrupt_edit=False):
        """
        Set current text value.
        
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


class MultilineTextEdit(QtWidgets.QPlainTextEdit):
    """
    Multi-line text edit.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    If ``continuous_update==True``, update signals are sent any time the content is edited;
    otherwise, they are sent only when the edit is done (i.e., focus is lost).
    """
    def __init__(self, parent, value=None, continuous_update=False):
        super().__init__(parent)
        self._value=None
        self._continuous_update=continuous_update
        if value is not None:
            self.set_value(value)
        self.textChanged.connect(self._on_change_text)
    def _on_text_update(self):
        text=self.toPlainText()
        if text!=self._value:
            self._value=text
            self.value_changed.emit(self._value)
        self.value_entered.emit(self._value)
    def _on_change_text(self):
        if self._continuous_update:
            self._on_text_update()
    def focusOutEvent(self, evt):
        if not self._continuous_update:
            self._on_text_update()
        super().focusOutEvent(evt)
    value_entered=Signal(object)
    """Signal emitted when value is entered (regardless of whether it stayed the same)"""
    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current text value"""
        return self._value
    def show_value(self, interrupt_edit=False):
        """
        Display currently stored text value
        
        If ``interrupt_edit==True`` and the edit is currently being modified by the user, don't update the display.
        """
        if (not self.hasFocus()) or interrupt_edit:
            self.setPlainText(self._value)
    def set_value(self, value, notify_value_change=True, interrupt_edit=False):
        """
        Set current text value.
        
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

class NumEdit(QtWidgets.QLineEdit):
    """
    Labview-style numerical edit.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    Supports different number representations, metric prefixes (in input or output), keyboard shortcuts (up/down for changing number, escape for cancelling).

    Args:
        parent: parent widget
        value: initial value (``None`` means no value is set)
        limiter: number limiter (for details, see :meth:`set_limiter`)
        formatter: number formatter (for details, see :meth:`set_formatter`)
        custom_steps: if not ``None``, can specify custom fixed value steps when up/down keys are pressed with a modifier key (Control, Alt, or Shift)
            specifies a dictionary ``{'ctrl':ctrl_step, 'alt':alt_step, 'shift':shift_step}`` with the corresponding steps (missing elements mean that the modifier key is ignored)
    """
    def __init__(self, parent, value=None, limiter=None, formatter=None, custom_steps=None):
        super().__init__(parent)
        self.limiter=as_limiter(limiter)
        self.formatter=as_formatter(formatter)
        self.custom_steps=custom_steps or {}
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
    def _on_change_text(self, text):  # pylint: disable=unused-argument
        if not self.isModified():
            try:
                value=str_to_float(str(self.text()))
                self.set_value(value)
            except ValueError:
                pass
    def keyPressEvent(self, event):
        k=event.key()
        m=event.modifiers()
        if k==QtCore.Qt.Key_Escape:
            self.show_value(interrupt_edit=True)
            self.clearFocus()
        elif k in [QtCore.Qt.Key_Up,QtCore.Qt.Key_Down]:
            try:
                step=None
                if m==QtCore.Qt.ControlModifier and "ctrl" in self.custom_steps:
                    step=self.custom_steps["ctrl"]
                elif m==QtCore.Qt.ShiftModifier and "shift" in self.custom_steps:
                    step=self.custom_steps["shift"]
                elif m==QtCore.Qt.AltModifier and "alt" in self.custom_steps:
                    step=self.custom_steps["alt"]
                else:
                    cursor_order=self.get_cursor_order()
                    if cursor_order!=None:
                        step=10**(cursor_order)
                if step is not None:
                    str_value=str(self.text())
                    num_value=str_to_float(str_value)
                    if k==QtCore.Qt.Key_Up:
                        self.set_value(num_value+step,interrupt_edit=True)
                    else:
                        self.set_value(num_value-step,interrupt_edit=True)
            except ValueError:
                self.show_value(interrupt_edit=True)
        else:
            super().keyPressEvent(event)
    def _read_input(self):
        try:
            return str_to_float(str(self.text()))
        except ValueError:
            return self._value

    def set_limiter(self, limiter, new_value=None):
        """
        Change current numerical limiter.

        Limiter can be a callable object which takes a single value and either returns a limited value, or raises :exc:`.limiter.LimitError` if it should be ignored;
        or it can be a tuple ``(lower, upper, action, value_type)``, where ``lower`` and ``upper`` are the limits (``None`` means no limits),
        ``action`` defines out-of-limit action (either ``"ignore"`` to ignore entered value, or ``"coerce"`` to truncate to the nearest limit),
        and ``value_type`` can be ``None`` (keep value as is), ``"float"`` (cast value to float), ``"int"`` (cast value to int).
        If the tuple is shorter, the missing parts are filled by default values ``(None, None, "ignore", None)``.
        """
        self.limiter=as_limiter(limiter)
        if new_value is None:
            new_value=self._value
        new_value=self._coerce_value(new_value,coerce_on_limit=True)
        if new_value!=self._value:
            self.set_value(new_value)
    def set_formatter(self, formatter):
        """
        Change current numerical formatter.

        Formatter can be a callable object turning value into a string, a string (``"float"``, ``"int"``, or a format string, e.g., ``".5f"``),
        or a tuple starting with ``"float"`` which contains arguments to the :class:`.formatter.FloatFormatter`.
        """
        self.formatter=as_formatter(formatter)
        self.show_value()
    def set_float_formatter(self, output_format="auto", digits=9, add_trailing_zeros=True, leading_zeros=0, explicit_sign=False):
        """
        Set up float formatter.

        Has the same functionality as :meth:`set_formatter` (i.e., ``set_float_formatter(*args)`` is equivalent to ``set_formatter(("float",)+args)``),
        but explicitly lists the arguments.

        Args:
            output_format(str): can be ``"auto"`` (use standard Python conversion), ``"SI"`` (use SI prefixes if possible), or ``"sci"`` (scientific "E" notation).
            digits (int): if ``add_trailing_zeros==False``, determines the number of significant digits; otherwise, determines precision (number of digits after decimal point).
            add_trailing_zeros (bool): if ``True``, always show fixed number of digits after the decimal point, with zero padding if necessary.
            leading_zeros (bool): determines the minimal size of the integer part (before the decimal point) of the number; pads with zeros if necessary.
            explicit_sign (bool): if ``True``, always add explicit plus sign.
        """
        self.set_formatter(("float",output_format,digits,add_trailing_zeros,leading_zeros,explicit_sign))
    def set_custom_steps(self, custom_steps=None):
        """
        Specify custom fixed value steps when up/down keys are pressed with a modifier key (Control, Alt, or Shift).

        `custom_steps` is a dictionary ``{'ctrl':ctrl_step, 'alt':alt_step, 'shift':shift_step}``
        with the corresponding steps (missing elements mean that the modifier key is ignored).
        """
        self.custom_steps=custom_steps or {}

    def get_cursor_order(self):
        """Get a decimal order of the text cursor"""
        str_value=str(self.text())
        cursor_pos=self.cursorPosition()
        return pos_to_order(str_value,cursor_pos)
    def set_cursor_order(self, order):
        """Move text cursor to a given decimal order"""
        if order is not None:
            new_cursor_pos=order_to_pos(str(self.text()),order)
            self.setCursorPosition(new_cursor_pos)

    def _coerce_value(self, value, coerce_on_limit=False):
        for _ in range(10):
            str_value=self.formatter(value)
            num_value=str_to_float(str_value)
            try:
                new_value=self.limiter(num_value)
            except LimitError:
                if coerce_on_limit and isinstance(self.limiter,NumberLimit):
                    if self.limiter.range[0] is not None and num_value<self.limiter.range[0]:
                        new_value=self.limiter.range[0]
                    else:
                        new_value=self.limiter.range[1]
                else:
                    raise
            if new_value==value:
                return new_value
            value=new_value
        raise ValueError("couldn't coerce the new value")
    def repr_value(self, value):
        """Return representation of `value` according to the current numerical format"""
        return self.formatter(value)

    value_entered=Signal(object)
    """Signal emitted when value is entered (regardless of whether it stayed the same)"""
    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current numerical value"""
        return self._value
    def show_value(self, interrupt_edit=False, preserve_cursor_order=True):
        """
        Display currently stored numerical value
        
        If ``interrupt_edit==False`` and the edit is currently being modified by the user, don't update the display.
        If ``preserve_cursor_order==True`` and the display value is being edited, keep the decimal order of the cursor position after change.
        """
        if (not self.hasFocus()) or interrupt_edit:
            if preserve_cursor_order and self.hasFocus():
                cursor_order=self.get_cursor_order()
                self.setText(self.formatter(self._value))
                if cursor_order is not None:
                    self.set_cursor_order(cursor_order)
            else:
                self.setText(self.formatter(self._value))
    def set_value(self, value, notify_value_change=True, interrupt_edit=False, preserve_cursor_order=True):
        """
        Set and display current numerical value.
        
        If ``notify_value_change==True``, emit the ``value_changed`` signal; otherwise, change value silently.
        If ``interrupt_edit==False`` and the edit is currently being modified by the user, don't update the display (but still update the internally stored value).
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
        except LimitError:
            pass
        self.show_value(interrupt_edit=interrupt_edit,preserve_cursor_order=preserve_cursor_order)
        return value_changed