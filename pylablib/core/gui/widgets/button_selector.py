from .. import QtWidgets, Signal
from ...utils.general import unique_class
from ..utils import clean_layout

class ButtonSelector(QtWidgets.QWidget):
    """
    Button selector widget.

    Similar to combo-box, but displays all options in a single row of buttons.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._layout=QtWidgets.QHBoxLayout(self)
        self._buttons=[]
        self._index=-1
        self._unselected_value=None
        self._index_values=None
        self._options=[]
        self._out_of_range_action="error"
        self._direct_index_action="ignore"
        self._event_only_on_changed=False
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
    keep=unique_class("keep")()
    none=unique_class("none")()
    def _display_index(self, index):
        for i,b in enumerate(self._buttons):
            if i!=index and b.isChecked():
                b.setChecked(False)
            if i==index and not b.isChecked():
                b.setChecked(True)
    def _get_displayed_index(self):
        for i,b in enumerate(self._buttons):
            if b.isChecked():
                return i
        return -1
    def _get_index_callback(self, i):
        def set_index():
            self._display_index(i)
            if self._index!=i or not self._event_only_on_changed:
                self._index=i
                self.value_changed.emit(self.index_to_value(self._index))
        return set_index
    def _set_buttons(self):
        self._clear_buttons()
        for i,l in enumerate(self._options):
            button=QtWidgets.QPushButton(self)
            button.setCheckable(True)
            button.clicked.connect(self._get_index_callback(i))
            button.setText(str(l))
            button.setObjectName("{}__b{}".format(self.objectName(),i))
            self._layout.addWidget(button,stretch=1)
            self._buttons.append(button)
    def _clear_buttons(self):
        self._buttons=[]
        clean_layout(self._layout)
    def iterbuttons(self):
        """Iterate over all selecting buttons"""
        for b in self._buttons:
            yield b
    def set_buttons_width(self, width):
        """Set the fixed width of all the buttons"""
        for b in self._buttons:
            b.setFixedWidth(width)
    def set_index_values(self, index_values, value=keep, index=None, unselected_value=keep):
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
            if len(index_values)!=len(self._options):
                raise ValueError("number of values {} is different from the number of options {}".format(len(index_values),len(self._options)))
            if self._unselected_value in index_values:
                raise ValueError("index values {} contain unselected value ({}), which is reserved to represent no selection".format(index_values,self._unselected_value))
        curr_value=self.get_value()
        self._index_values=index_values
        if value is not ButtonSelector.keep:
            self.set_value(value)
        elif index is not None:
            self.set_value(self.get_index_values()[index])
        else:
            self._index=-1
            self._display_index(-1)
            try:
                self.set_value(curr_value)
            except ValueError:
                pass
    def get_index_values(self):
        """Return the list of values corresponding to combo box indices"""
        return list(self._index_values) if self._index_values is not None else list(range(len(self._options)))
    def get_options(self):
        """Return the list of labels corresponding to combo box indices"""
        return list(self._options)
    def get_options_dict(self):
        """Return the dictionary ``{value: label}`` of the option labels"""
        return dict(zip(self.get_index_values(),self._options))
    def set_options(self, options, index_values=None, value=keep, index=None, unselected_value=keep):
        """
        Set new set of options.

        If `index_values` is not ``None``, set these as the new index values; otherwise, index values are reset.
        If `options` is a dictionary, interpret it as a mapping ``{option: index_value}``.
        If `value` is specified, set as the new values.
        If `index` is specified, use it as the index of a new value; if both `value` and `index` are specified, the `value` takes priority.
        If `unselected_value` is supplied, it specifies which value corresponds to no combo box value being selected (by default, keep the current value).
        """
        if isinstance(options,dict):
            index_values=list(options)
            options=[options[v] for v in index_values]
        else:
            if index_values is None:
                index_values=list(range(len(options)))
        self._options=options
        self._set_buttons()
        self.set_index_values(index_values,value=value,index=index,unselected_value=unselected_value)
    
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
        if not self._options or value==self._unselected_value:
            return False
        index=self.value_to_index(value)
        if self._out_of_range_action=="ignore" and index==-1:
            return False
        index=max(-1,min(index,len(self._index_values)-1))
        if self._index!=index:
            self._index=index
            self._display_index(index)
            if notify_value_change:
                self.value_changed.emit(self.index_to_value(self._index))
            return True
        else:
            return False
    def repr_value(self, value):
        """Return representation of `value` as a combo box text"""
        index=self.value_to_index(value)
        if index<0:
            return "N/A"
        return self._options[index]