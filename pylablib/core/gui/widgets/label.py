from .. import QtWidgets, Signal

from ..limiter import as_limiter, LimitError, NumberLimit
from ..formatter import as_formatter, str_to_float



class TextLabel(QtWidgets.QLabel):
    """
    Labview-style text label.

    The main difference from the standard ``QLabel`` is the changed event.
    """
    def __init__(self, parent, value=None):
        super().__init__(parent)
        self._value=None
        if value is not None:
            self.set_value(value)
    clicked=Signal()
    def mousePressEvent(self, ev):
        self.clicked.emit()
        return super().mousePressEvent(ev)
    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current numerical value"""
        return self._value
    def set_value(self, value):
        """Set and display current text value"""
        if value is not None:
            if self._value!=value:
                self._value=value
                self.setText(str(self._value))
                self.value_changed.emit(self._value)



class EnumLabel(QtWidgets.QLabel):
    """
    Labview-style label for enumerated values.

    Can automatically convert input enum values into corresponding text labels based on the `options` dictionary.
    Can also specify a function which takes a single value argument and converts into a enum value before checking `options`;
    useful for "fuzzy" options (e.g., when 0 and ``False`` mean the same thing)
    """
    def __init__(self, parent, options, value=None, prep=None):
        super().__init__(parent)
        self._value=None
        self._options=options if isinstance(options,dict) else dict(zip(range(len(options)),options))
        self._out_of_range_action="error"
        self._prep=prep
        if value is not None:
            self.set_value(value)
    clicked=Signal()
    def mousePressEvent(self, ev):
        self.clicked.emit()
        return super().mousePressEvent(ev)
    def set_out_of_range(self, action="error"):
        """
        Set behavior when out-of-range value is applied.

        Can be ``"error"`` (raise error), ``"text"`` (turn value into text and display it), or ``"ignore"`` (keep current value).
        """
        if action not in ["error","text","ignore"]:
            raise ValueError("unrecognized out-of-range action: {}".format(action))
        self._out_of_range_action=action
    def set_options(self, options, value=None, index=None):
        """
        Set new set of options.

        If `index_values` is not ``None``, set these as the new index values; otherwise, index values are reset.
        If `options` is a dictionary, interpret it as a mapping ``{option: index_value}``.
        If `value` is specified, set as the new values.
        If `index` is specified, use it as the index of a new value; if both `value` and `index` are specified, the `value` takes priority.
        """
        self._options=options if isinstance(options,dict) else dict(zip(range(len(options)),options))
        if value is not None:
            self.set_value(value)
        elif index is not None:
            self.set_value(list(self._options)[index])
        else:
            self.set_value(self._value)
    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current numerical value"""
        return self._value
    def _prepare_value(self, value):
        if self._prep is not None:
            value=self._prep(value)
        if value not in self._options:
            if self._out_of_range_action=="ignore":
                return None
            elif self._out_of_range_action=="error":
                raise ValueError("value {} is not among available option {}".format(value,list(self._options)))
            else:
                value=str(value)
        return value
    def set_value(self, value):
        """Set and display current text value"""
        if value is not None:
            value=self._prepare_value(value)
            if value is None:
                return
            self.setText(self._options.get(value,value))
            if self._value!=value:
                self._value=value
                self.value_changed.emit(self._value)
    def repr_value(self, value):
        """Return representation of `value` as a combo box text"""
        if value is not None:
            value=self._prepare_value(value)
            if value is None:
                return None
            return self._options.get(value,value)



class NumLabel(QtWidgets.QLabel):
    """
    Labview-style numerical label.

    Supports different number representations and metric prefixes.

    Args:
        parent: parent widget
        value: initial value (``None`` means no value is set)
        limiter: number limiter (for details, see :meth:`set_limiter`)
        formatter: number formatter (for details, see :meth:`set_formatter`)
        allow_text: if ``True``, can also take text values (which are displayed as is); otherwise, raise an error.
    """
    def __init__(self, parent, value=None, limiter=None, formatter=None, allow_text=True):
        super().__init__(parent)
        self.limiter=as_limiter(limiter)
        self.formatter=as_formatter(formatter)
        self._value=None
        self.allow_text=allow_text
        if value is not None:
            self.set_value(value)
            
    clicked=Signal()
    def mousePressEvent(self, ev):
        self.clicked.emit()
        return super().mousePressEvent(ev)
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
        self.set_value(None)
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

    value_changed=Signal(object)
    """Signal emitted when value is changed"""
    def get_value(self):
        """Get current numerical value"""
        return self._value
    def set_value(self, value):
        """Set and display current numerical value"""
        if value is not None:
            if self._value==value:
                return True
            try:
                if isinstance(value,str):
                    if self.allow_text:
                        self._value=value
                        self.setText(self._value)
                    else:
                        raise ValueError("this label doesn't accept text values")
                else:
                    value=self.limiter(value)
                    self._value=value
                    self.setText(self.formatter(self._value))
                self.value_changed.emit(self._value)
                return True
            except LimitError:
                pass
        if self._value is not None:
            self.setText(self.formatter(self._value))
        return False