class LimitError(ArithmeticError):
    """Error raised when the value is out of limits and can't be coerced."""
    def __init__(self, value, lower_limit=None, upper_limit=None):
        self.value=value
        self.lower_limit=lower_limit
        self.upper_limit=upper_limit
    def __str__(self):
        lb=self.lower_limit
        if lb==None:
            lb="-Inf"
        hb=self.upper_limit
        if hb==None:
            hb="+Inf"
        return "value {0} is out of limits ({1}, {2})".format(self.value, lb,hb)
class NumberLimit(object):
    """
    Number limiter, which checks validity of user inputs.

    Callable object with takes a number as an argument and either returns its coerced version (or the number itself, if it is within limits),
    or raises :exc:`LimitError` if it should be ignored.

    Args:
        lower_limit: lower limit (inclusive), or ``None`` if there is no limit.
        upper_limit: upper limit (inclusive), or ``None`` if there is no limit.
        action (str): action taken if the number is out of limits; either ``"coerce"`` (return the closest valid value),
            or ``"ignore"`` (raise :exc:`LimitError`).
        value_type (str): determines value type coercion; can be ``None`` (do nothing, only check limits), ``"float"`` (cast to float), or ``"int"`` (cast to integer).
    """
    def __init__(self, lower_limit=None, upper_limit=None, action="ignore", value_type=None):
        object.__init__(self)
        if not value_type in [None,"float","int"]:
            raise ValueError("unrecognized value type: {0}".format(value_type))
        self.value_type=value_type
        lower_limit,upper_limit=self.cast(lower_limit), self.cast(upper_limit)
        if lower_limit!=None and upper_limit!=None and lower_limit>upper_limit:
            raise ValueError("impossible value range: ({0}, {1})".format(lower_limit,upper_limit))
        self.range=(lower_limit,upper_limit)
        if not action in ["coerce", "ignore"]:
            raise ValueError("unrecognized action: {0}".format(action))
        self.action=action
    def __call__(self, value):
        """
        Restrict value to the preset limit and type.
        Raise LimitError if value is outside bounds and action=='ignore'.
        """
        value=self.cast(value)
        if self.range[0] is not None and value<self.range[0]:
            if self.action=="coerce":
                return self.cast(self.range[0])
            elif self.action=="ignore":
                raise LimitError(value,*self.range)
        elif self.range[1] is not None and value>self.range[1]:
            if self.action=="coerce":
                return self.cast(self.range[1])
            elif self.action=="ignore":
                raise LimitError(value,*self.range)
        else:
            return value
    def cast(self, value):
        if value==None:
            return None
        if self.value_type=="float":
            return float(value)
        elif self.value_type=="int":
            return int(value)
        else:
            return value

def filter_limiter(pred):
    """
    Turn a predicator into a limiter.

    Returns a function that raises :exc:`LimitError` if the predicate is false.
    """
    def wrapped(v):
        if not pred(v):
            raise LimitError(v)
        return v
    return wrapped

def as_limiter(limiter):
    """
    Turn an object into a limiter.

    Can be a callable object (returned as is) or a tuple which is used as a list of arguments to the :class:`NumberLimit` object.
    """
    if hasattr(limiter,"__call__"):
        return limiter
    if isinstance(limiter,tuple):
        return NumberLimit(*limiter)
    raise ValueError("unknown limiter: {}".format(limiter))