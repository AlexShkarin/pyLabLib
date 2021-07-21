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
        self._out_of_range_action="error"
    def set_out_of_range(self, action="error"):
        """
        Set behavior when out-of-range value is applied.

        Can be ``"error"`` (raise error), ``"reset"`` (reset to no-value position), or ``"ignore"`` (keep current value).
        """
        if action not in ["error","reset","ignore"]:
            raise ValueError("unrecognized out-of-range action: {}".format(action))
        self._out_of_range_action=action
    def index_to_value(self, idx):
        """Turn numerical index into value"""
        if (self._index_values is None) or (idx<0) or (idx>=len(self._index_values)):
            return idx
        else:
            return self._index_values[idx]
    def value_to_index(self, value):
        """Turn value into a numerical index"""
        try:
            return value if (value==-1 or self._index_values is None) else self._index_values.index(value)
        except ValueError as err:
            if self._out_of_range_action=="error":
                raise ValueError("value {} is not among available option {}".format(value,self._index_values)) from err
            return -1
    def _on_index_changed(self, index):
        if self._index!=index:
            self._index=index
            self.value_changed.emit(self.index_to_value(self._index))
    def set_index_values(self, index_values, value=None):
        """
        Set a list of values corresponding to combo box indices.

        Can be either a list of values, whose length must be equal to the number of options, or ``None`` (simply use indices).
        Note: if the number of combo box options changed (e.g., using ``addItem`` or ``insertItem`` methods),
        the index values need to be manually updated; otherwise, the errors might arise if the index is larger than the number of values.
        """
        if index_values is not None:
            if len(index_values)!=self.count():
                raise ValueError("number of values {} is different from the number of options {}".format(len(index_values),self.count()))
            if -1 in index_values:
                raise ValueError("index values {} contain -1, which is reserved to represent no selection".format(index_values))
        curr_value=self.get_value()
        self._index_values=index_values
        if value is not None:
            self.set_value(value)
        else:
            self._index=-1
            self.setCurrentIndex(-1)
            try:
                self.set_value(curr_value)
            except ValueError:
                pass
    def set_options(self, options, index_values=None, value=None):
        """
        Set new set of options.

        If `index_values` is not ``None``, set these as the new index values; otherwise, index values are reset.
        """
        while self.count():
            self.removeItem(0)
        self.addItems(options)
        self.set_index_values(index_values,value=value)

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
        if not self.count() or value==-1:
            return False
        index=self.value_to_index(value)
        if self._out_of_range_action=="ignore" and index==-1:
            return False
        index=max(-1,min(index,self.count()-1))
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
        if value==-1:
            return "N/A"
        index=self.value_to_index(value)
        return self.itemText(index)