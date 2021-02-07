from PyQt5 import QtWidgets, QtCore

class ToggleButton(QtWidgets.QPushButton):
    """
    Expanded toggle button.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    Allows setting different captions of pressed/unpressed, and uses those to represent values.
    """
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setCheckable(True)
        self.clicked.connect(self._on_clicked)
        self._value=False
        self._labels=None
    def _get_label_text(self, value):
        return self._labels[int(bool(value))] if self._labels else None
    def _display_value(self):
        self.setChecked(self._value)
        caption=self._get_label_text(self._value)
        if caption is not None:
            self.setText(caption)
    def _on_clicked(self, value):
        if self._value!=value:
            self._value=value
            self._display_value()
            self.value_changed.emit(self._value)
    def set_value_labels(self, labels):
        """
        Set a list of values corresponding to combo box indices.

        Can be either a list of values, whose length must be equal to the number of options, or ``None`` (don't change the button label on toggle).
        """
        if labels is not None and len(labels)!=2:
            raise ValueError("two labels should be supplied, received {}".format(len(labels)))
        self._labels=labels
        self._display_value()

    value_changed=QtCore.pyqtSignal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current numerical value"""
        return self._value
    def set_value(self, value, notify_value_change=True):
        """
        Set current value.
        
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        """
        value=bool(value)
        if self._value!=value:
            self._value=value
            self._display_value()
            if notify_value_change:
                self.value_changed.emit(self._value)
            return True
        else:
            return False
    def repr_value(self, value):
        """Return representation of `value` as a combo box text"""
        caption=self._get_label_text(value)
        if caption is not None:
            return caption
        else:
            return ["Off","On"][int(bool(value))]