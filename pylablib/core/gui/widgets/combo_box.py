from .. import QtWidgets, Signal
from ...utils.general import unique_class

class ComboBox(QtWidgets.QComboBox):
    """
    Expanded combo box.

    Maintains internally stored consistent value (which can be, e.g., accessed from different threads).
    Allows setting values which are reported via ``value_changed`` signal instead of simple indices.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.activated.connect(self._on_index_changed)
        self._index=-1
        self._unselected_value=-1
        self._index_values=None
        self._out_of_range_action="error"
        self._direct_index_action="ignore"
    def wheelEvent(self, event):
        event.ignore()
    def set_out_of_range(self, action="error"):
        """
        Set behavior when out-of-range value is applied.

        Can be ``"error"`` (raise error), ``"reset"`` (reset to no-value position), ``"reset_start"`` (reset to the first position) or ``"ignore"`` (keep current value).
        """
        if action not in ["error","reset","reset_start","ignore"]:
            raise ValueError("unrecognized out-of-range action: {}".format(action))
        self._out_of_range_action=action
    def set_direct_index_action(self, action="error"):
        """
        Set behavior when index values are specified, but direct indexing is used.

        Can be ``"ignore"`` (do not allow direct indexing and treat any value as index value),
        ``"value_default"`` (allow direct indexing, but prioritize index values with the same value),
        or ``"index_default"`` (allow direct indexing and prioritize it if index value with the same value exists).
        """
        if action not in ["ignore","value_default","index_default"]:
            raise ValueError("unrecognized direct index action: {}".format(action))
        self._direct_index_action=action
    def index_to_value(self, idx):
        """Turn numerical index into value"""
        if (self._index_values is None) or (idx<-1) or (idx>=len(self._index_values)):
            return idx
        elif idx==-1:
            return self._unselected_value
        else:
            return self._index_values[idx]
    def value_to_index(self, value):
        """Turn value into a numerical index"""
        try:
            if value==self._unselected_value:
                return -1
            if self._index_values is None:
                return value
            if isinstance(value,int) and value>=0 and value<len(self._index_values):
                if self._direct_index_action=="value_default" and value in self._index_values:
                    return self._index_values.index(value)
                if self._direct_index_action!="ignore":
                    return value
            return self._index_values.index(value)
        except ValueError as err:
            if self._out_of_range_action=="error":
                raise ValueError("value {} is not among available options {}".format(value,self._index_values)) from err
            if self._out_of_range_action=="reset_start":
                return 0
            return -1
    def _on_index_changed(self, index):
        if self._index!=index:
            self._index=index
            self.value_changed.emit(self.index_to_value(self._index))
    keep=unique_class("keep")()
    none=unique_class("none")()
    def set_index_values(self, index_values, value=None, index=None, unselected_value=keep):
        """
        Set a list of values corresponding to combo box indices.

        Can be either a list of values, whose length must be equal to the number of options, or ``None`` (simply use indices).
        Note: if the number of combo box options changed (e.g., using ``addItem`` or ``insertItem`` methods),
        the index values need to be manually updated; otherwise, the errors might arise if the index is larger than the number of values.
        If `value` is specified, set as the new values.
        If `index` is specified, use it as the index of a new value; if both `value` and `index` are specified, the `value` takes priority.
        If `unselected_value` is supplied, it specifies which value corresponds to no combo box value being selected (by default, keep the current value).
        """
        if unselected_value is not self.keep:
            self._unselected_value=unselected_value
        if index_values is not None:
            if len(index_values)!=self.count():
                raise ValueError("number of values {} is different from the number of options {}".format(len(index_values),self.count()))
            if self._unselected_value in index_values:
                raise ValueError("index values {} contain unselected value ({}), which is reserved to represent no selection".format(index_values,self._unselected_value))
        curr_value=self.get_value()
        self._index_values=index_values
        if value is not None:
            self.set_value(value)
        elif index is not None:
            self.set_value(self.get_index_values()[index])
        else:
            self._index=-1
            self.setCurrentIndex(-1)
            try:
                self.set_value(curr_value)
            except ValueError:
                pass
    def get_index_values(self):
        """Return the list of values corresponding to combo box indices"""
        return list(self._index_values) if self._index_values is not None else list(range(self.count()))
    def get_options(self):
        """Return the list of labels corresponding to combo box indices"""
        return [self.itemText(i) for i in range(self.count())]
    def get_options_dict(self):
        """Return the dictionary ``{value: label}`` of the option labels"""
        return dict(zip(self.get_index_values(),self.get_options()))
    def set_options(self, options, index_values=None, value=None, index=None, unselected_value=keep):
        """
        Set new set of options.

        If `index_values` is not ``None``, set these as the new index values; otherwise, index values are reset.
        If `options` is a dictionary, interpret it as a mapping ``{option: index_value}``.
        If `value` is specified, set as the new values.
        If `index` is specified, use it as the index of a new value; if both `value` and `index` are specified, the `value` takes priority.
        If `unselected_value` is supplied, it specifies which value corresponds to no combo box value being selected (by default, keep the current value).
        """
        while self.count():
            self.removeItem(0)
        if isinstance(options,dict):
            index_values=list(options)
            options=[options[v] for v in index_values]
        self.addItems(options)
        self.set_index_values(index_values,value=value,index=index,unselected_value=unselected_value)
    def insert_option(self, option, index_value=None, index=None):
        """
        Insert or append a new option to the list
        
        Insertion (i.e., ``index is not None``) only works for index-valued combo boxes.
        """
        if self._index_values is None:
            if index is not None:
                raise ValueError("insertion only works for index-valued combo boxes")
            self.set_options(self.get_options()+[option])
        else:
            if index_value is None:
                raise ValueError("can not add None-valued element")
            options,index_values=self.get_options(),self.get_index_values()
            index=len(index_values) if index is None else index
            options.insert(index,option)
            index_values.insert(index,index_value)
            self.set_options(options,index_values)

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
        if not self.count() or value==self._unselected_value:
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
        if value==self._unselected_value:
            return "N/A"
        index=self.value_to_index(value)
        return self.itemText(index)