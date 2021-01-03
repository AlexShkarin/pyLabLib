from PyQt5 import QtWidgets, QtCore

from ..limiter import as_limiter, LimitError, NumberLimit
from ..formatter import as_formatter, str_to_float



class LVTextLabel(QtWidgets.QLabel):
    """
    Labview-style text label.

    The main difference from the standard :cls:`QLabel` is the changed event.
    """
    def __init__(self, parent, value=None):
        QtWidgets.QLabel.__init__(self, parent)
        self._value=None
        if value is not None:
            self.set_value(value)
    value_changed=QtCore.pyqtSignal(object)
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



class LVNumLabel(QtWidgets.QLabel):
    """
    Labview-style numerical label.

    Supports different number representations and metric perfixes.

    Args:
        parent: parent widget
        value: initial value (``None`` means no value is set)
        limiter: number limiter (for details, see :meth:`set_limiter`)
        formatter: number formatter (for details, see :meth:`set_formatter`)
        allow_text: if ``True``, can also take text values (which are displayed as is); otherwise, raise an error.
    """
    def __init__(self, parent, value=None, limiter=None, formatter=None, allow_text=True):
        QtWidgets.QLabel.__init__(self, parent)
        self.limiter=as_limiter(limiter)
        self.formatter=as_formatter(formatter)
        self._value=None
        self.allow_text=allow_text
        if value is not None:
            self.set_value(value)
            
    def set_limiter(self, limiter, new_value=None):
        """
        Change current numerical limiter.

        Limiter can be a callable object which takes a single value and either returns a limited value, or raises :exc:`LimitError` if it should be ignored;
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

        Formatter can be a callable object turining value into a string, a string (``"float"``, ``"int"``, or a format string, e.g., ``".5f"``),
        or a tuple starting with ``"float"`` which contains arguments to the :class:`FloatFormatter`.
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

    value_changed=QtCore.pyqtSignal(object)
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