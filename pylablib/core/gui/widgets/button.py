from .. import QtWidgets, QtCore, Signal

class ToggleButton(QtWidgets.QPushButton):
    """
    Expanded toggle button.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    Allows setting different captions of pressed/unpressed, and uses those to represent values.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
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

    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current value"""
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
        """Return representation of `value` as a caption text"""
        caption=self._get_label_text(value)
        if caption is not None:
            return caption
        else:
            return ["Off","On"][int(bool(value))]



class DropdownButton(QtWidgets.QToolButton):
    """
    Button which shows a dropdown menu.

    Implements simple methods for generating a simple single-level menu.
    Changed signal is called with a single parameter, which is the menu item name.
    Getting value always returns ``None``, setting value generates a value event (i.e., simulates clicks).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        menu=QtWidgets.QMenu("menu",parent=self)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setStyleSheet('QToolButton::menu-indicator {image: none}')
        self.setMenu(menu)
        menu.triggered.connect(self._on_clicked)
        self._items={}
    def add_item(self, name, text):
        """Add a new menu item"""
        if name in self._items:
            raise ValueError("item {} already exists".format(name))
        self._items[name]=self.menu().addAction(text)
    def remove_item(self, name):
        """Remove an existing menu item"""
        if name not in self._items:
            raise ValueError("item {} does not exist".format(name))
        self.removeAction(self.items.pop(name))
    def _on_clicked(self, action):
        for n,s in self._items.items():
            if s is action:
                self.value_changed.emit(n)
                return

    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get value (always return ``None``, added for compatibility)"""
        return None
    def set_value(self, value):
        """Get value (emits a signal if the value is among the items)"""
        if value is None:
            return
        if value not in self._items:
            raise ValueError("item {} does not exist".format(value))
        self.value_changed.emit(value)
    def repr_value(self, value):
        """Represent a value as a corresponding label"""
        return self._items[value].text() if value in self._items else ""