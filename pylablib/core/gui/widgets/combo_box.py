from .. import QtWidgets, Signal

class ComboBox(QtWidgets.QComboBox):
    """
    Expanded combo box.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    Allows setting values which are reported via ``value_changed`` signal instead of simple indices.
    """
    def __init__(self, parent):
        QtWidgets.QComboBox.__init__(self, parent)
        self.activated.connect(self._on_index_changed)
        self._index=-1
        self._index_values=None
    def index_to_value(self, idx):
        """Turn numerical index into value"""
        if (self._index_values is None) or (idx<0) or (idx>=len(self._index_values)):
            return idx
        else:
            return self._index_values[idx]
    def value_to_index(self, value):
        """Turn value into a numerical index"""
        try:
            return value if self._index_values is None else self._index_values.index(value)
        except ValueError as err:
            raise ValueError("value {} is not among available option {}".format(value,self._index_values)) from err
    def _on_index_changed(self, index):
        if self._index!=index:
            self._index=index
            self.value_changed.emit(self.index_to_value(self._index))
    def set_index_values(self, values):
        """
        Set a list of values corresponding to combo box indices.

        Can be either a list of values, whose length must be equal to the number of options, or ``None`` (simply use indices).
        Note: if the number of combo box options changed (e.g., using ``addItem`` or ``insertItem`` methods),
        the index values need to be manually updated; otherwise, the errors might arise if the index is large than the number of values.
        """
        if values is not None and len(values)!=self.count():
            raise ValueError("number of values {} is different from the number of options {}".format(len(values),self.count()))
        self._index_values=values

    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current numerical value"""
        return self.index_to_value(self._index)
    def set_value(self, value, notify_value_change=True):
        """
        Set current value.
        
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        """
        if not self.count():
            return
        index=max(0,min(self.value_to_index(value),self.count()-1))
        if self._index!=index:
            self._index=index
            self.setCurrentIndex(self._index)
            if notify_value_change:
                self.value_changed.emit(self.index_to_value(self._index))
            return True
        else:
            return False
    def repr_value(self, value):
        """Return representation of `value` as a combo box text"""
        index=self.value_to_index(value)
        return self.itemText(index)