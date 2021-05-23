"""
Contains routines for checking arguments passed into a function for better flexibility. 
"""

from .py3 import textstring

import numpy as np


_default_parameter_error_message="unrecognized value of a parameter '{1}': '{0}'"
def parameter_value_error(par_val, par_name, message=None, error_type=None):
    """
    Raise parameter value error (:exc:`ValueError` by default).
    """
    error_type=error_type or ValueError
    message=message or _default_parameter_error_message
    raise error_type(message.format(par_val,par_name))

_default_parameter_range_error_message=_default_parameter_error_message+"; acceptable values are {2}"
def parameter_range_error(par_val, par_name, par_set=None, message=None, error_type=None):
    """
    Raise parameter range error (:exc:`ValueError` by default).
    """
    if par_set is None:
        parameter_value_error(par_val,par_name,message,error_type)
    error_type=error_type or ValueError
    message=message or _default_parameter_range_error_message
    raise error_type(message.format(par_val,par_name,list(par_set)))

def check_parameter_range(par_val, par_name, par_set, message=None, error_type=None):
    """
    Raise error if `par_val` is not in in the `par_set` (`par_name` is used in the error message).
    """
    if not (par_val in par_set):
        parameter_range_error(par_val,par_name,par_set,message,error_type)
        
        
_default_parameter_disagreeing_message="assigned value {1} doesn't agree with the current values {0}"
def getdefault(value, default_value, unassigned_value=None, conflict_action="ignore", message=None, error_type=None):
    """
    Analog of ``dict``'s ``getdefault``.
    
    If `value` is `unassigned_value`, return `default_value` instead.
    If ``conflict_action=='error'`` and ``value!=default_value``, raise value error using `message` and `error_type`.
    """
    if unassigned_value is None:
        unassigned=value is None
    else:
        unassigned=(value==unassigned_value)
    if unassigned:
        return default_value
    elif value!=default_value:
        check_parameter_range(conflict_action,"conflict_action",{"ignore","error"})
        if conflict_action=="error":
            error_type=error_type or ValueError
            message=message or _default_parameter_disagreeing_message
            raise error_type(message.format(value,default_value))
    return value




def is_sequence(value, sequence_type="builtin;nostring"):
    """
    Check if `value` is a sequence.
    
    `sequence_type` is semicolon separated list of possible sequence types:
        - ``'builtin'`` - ``list``, ``tuple`` or ``str``
        - ``'nostring'`` - ``str`` is not allows
        - ``'array'`` - ``list``, ``tuple`` or ``numpy.ndarray``
        - ``'indexable'`` - anything which can be indexed
        - ``'haslength'`` - anything with length property
    """
    try:
        iter(value) # iter is supported by any object having __getitem__ or __iter__
    except TypeError:
        return False
    sequence_types=sequence_type.split(";")
    for st in sequence_types:
        if st=="builtin":
            if not (isinstance(value,list) or isinstance(value,tuple) or isinstance(value,textstring)):
                return False
        elif st=="nostring":
            if isinstance(value,textstring):
                return False
        elif st=="array":
            if not (isinstance(value,list) or isinstance(value,tuple) or isinstance(value,np.ndarray)):
                return False
        elif st=="indexable":
            try:
                value[0]
            except (IndexError,ValueError,KeyError):
                pass
            except TypeError:
                return False
        elif st=="haslength":
            try:
                len(value)
            except TypeError:
                return False
        else:
            check_parameter_range(st,"sequence_type",{"builtin","indexable","nostring","haslength","array"})
    return True
def make_sequence(element, length=1, sequence_type="list"):
    """
    Turn element into a sequence of `sequence_type` (``'list'`` or ``'tuple'``) repeated `length` times.
    """
    check_parameter_range(sequence_type,"sequence_type",{"list","tuple"})
    if sequence_type=="list":
        return [element]*length
    elif sequence_type=="tuple":
        return (element,)*length
_default_length_disagreeing_message="length of a parameter {0} doesn't agree with the expected length {1}"
def as_sequence(value, multiply_length=1, allowed_type="builtin;nostring", wrapping_type="list", length_conflict_action="ignore", message=None, error_type=None):
    """
    Ensure that `value` is a sequence.
    
    If `value` is not a sequence of `allowed_type` (as checked by :func:`is_sequence`), turn it into a sequence specified by `wrapping_type` and `multiply_length`.
    
    If value is a sequence and ``length_conflict_action=='error'``, raise error with `error_type` and `error_message` if the length doesn't match `multiply_length`.
    Otherwise, return value unchanged.
    """
    if is_sequence(value,sequence_type=allowed_type):
        if len(value)!=multiply_length:
            check_parameter_range(length_conflict_action,"length_conflict_action",{"ignore","error"})
            if length_conflict_action=="error":
                error_type=error_type or ValueError
                message=message or _default_length_disagreeing_message
                raise error_type(message.format(value,multiply_length))
        return value
    else:
        return make_sequence(value,length=multiply_length,sequence_type=wrapping_type)