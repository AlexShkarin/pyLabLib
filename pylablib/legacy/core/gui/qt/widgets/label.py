from PyQt5 import QtWidgets
from ... import format,limit

class LVNumLabel(QtWidgets.QLabel):
    """
    Labview-style numerical label.

    Supports different number representations and metric perfixes.
    """
    def __init__(self, parent, value=None, num_limit=None, num_format=None, allow_text=True):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.num_limit=limit.as_limiter(num_limit) if num_limit is not None else limit.NumberLimit()
        self.num_format=format.as_formatter(num_format) if num_format is not None else format.FloatFormatter()
        self._value=None
        self.allow_text=allow_text
        if value is not None:
            self.set_value(value)
            
    def change_limiter(self, limiter):
        """Change current numerical limiter"""
        self.num_limit=limit.as_limiter(limiter)
        self.set_value(self._value)
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
        self.set_value(None)
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
    
    def repr_value(self, value):
        """Return representation of `value` according to the current numerical format"""
        return self.num_format(value)

    def get_value(self):
        """Get current numerical value"""
        return self._value
    def set_value(self, value):
        """Set and display current numerical value"""
        if value is not None:
            try:
                if isinstance(value,str):
                    if self.allow_text:
                        self._value=value
                        self.setText(self._value)
                    else:
                        raise ValueError("this label doesn't accept text values")
                else:
                    value=self.num_limit(value)
                    self._value=value
                    self.setText(self.num_format(self._value))
                return True
            except limit.LimitError:
                pass
        if self._value is not None:
            self.setText(self.num_format(self._value))
        return False