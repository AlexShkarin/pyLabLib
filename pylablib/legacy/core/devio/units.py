"""
Routines for conversion of physical units.
"""

from __future__ import division

import numpy as np
from ..utils import string as string_utils  #@UnresolvedImport
import re
    

def split_units(value):
    """
    Split string dimensionful value.

    Return tuple ``(val, unit)``, where ``val`` is the float part of the value, and ``unit`` is the string representing units.
    """
    m=re.match(r"([+-.\d]+)\s*([a-zA-Z]*)$",value)
    if not m:
        raise ValueError("can't parse value {}".format(value))
    return float(m[1]),m[2]
def convert_length_units(value, value_unit="m", result_unit="m", case_sensitive=True):
    """
    Convert `value` from `value_unit` to `result_unit`.
    
    The possible length units are ``'m'``,``'mm'``, ``'um'``, ``'nm'``, ``'pm'``, ``'fm'``.
    If ``case_sensitive==True``, matching units is case sensitive. 
    """
    if string_utils.string_equal(value_unit,"m",case_sensitive=case_sensitive):
        value_m=value
    elif string_utils.string_equal(value_unit,"mm",case_sensitive=case_sensitive):
        value_m=value*1E-3
    elif string_utils.string_equal(value_unit,"um",case_sensitive=case_sensitive):
        value_m=value*1E-6
    elif string_utils.string_equal(value_unit,"nm",case_sensitive=case_sensitive):
        value_m=value*1E-9
    elif string_utils.string_equal(value_unit,"pm",case_sensitive=case_sensitive):
        value_m=value*1E-12
    elif string_utils.string_equal(value_unit,"fm",case_sensitive=case_sensitive):
        value_m=value*1E-15
    else:
        raise IOError("unrecognized length unit: {0}".format(value_unit))
    if string_utils.string_equal(result_unit,"m",case_sensitive=case_sensitive):
        return value_m
    elif string_utils.string_equal(result_unit,"mm",case_sensitive=case_sensitive):
        return value_m*1E3
    elif string_utils.string_equal(result_unit,"um",case_sensitive=case_sensitive):
        return value_m*1E6
    elif string_utils.string_equal(result_unit,"nm",case_sensitive=case_sensitive):
        return value_m*1E9
    elif string_utils.string_equal(result_unit,"pm",case_sensitive=case_sensitive):
        return value_m*1E12
    elif string_utils.string_equal(result_unit,"fm",case_sensitive=case_sensitive):
        return value_m*1E15
    else:
        raise IOError("unrecognized length unit: {0}".format(result_unit))
    
def convert_time_units(value, value_unit="s", result_unit="s", case_sensitive=True):
    """
    Convert `value` from `value_unit` to `result_unit`.
    
    The possible time units are ``'s'``,``'ms'``, ``'us'``, ``'ns'``, ``'ps'``, ``'fs'``, ``'as'``.
    If ``case_sensitive==True``, matching units is case sensitive. 
    """
    if string_utils.string_equal(value_unit,"s",case_sensitive=case_sensitive):
        value_s=value
    elif string_utils.string_equal(value_unit,"ms",case_sensitive=case_sensitive):
        value_s=value*1E-3
    elif string_utils.string_equal(value_unit,"us",case_sensitive=case_sensitive):
        value_s=value*1E-6
    elif string_utils.string_equal(value_unit,"ns",case_sensitive=case_sensitive):
        value_s=value*1E-9
    elif string_utils.string_equal(value_unit,"ps",case_sensitive=case_sensitive):
        value_s=value*1E-12
    elif string_utils.string_equal(value_unit,"fs",case_sensitive=case_sensitive):
        value_s=value*1E-15
    elif string_utils.string_equal(value_unit,"as",case_sensitive=case_sensitive):
        value_s=value*1E-18
    else:
        raise IOError("unrecognized length unit: {0}".format(value_unit))
    if string_utils.string_equal(result_unit,"s",case_sensitive=case_sensitive):
        return value_s
    elif string_utils.string_equal(result_unit,"ms",case_sensitive=case_sensitive):
        return value_s*1E3
    elif string_utils.string_equal(result_unit,"us",case_sensitive=case_sensitive):
        return value_s*1E6
    elif string_utils.string_equal(result_unit,"ns",case_sensitive=case_sensitive):
        return value_s*1E9
    elif string_utils.string_equal(result_unit,"ps",case_sensitive=case_sensitive):
        return value_s*1E12
    elif string_utils.string_equal(result_unit,"fs",case_sensitive=case_sensitive):
        return value_s*1E15
    elif string_utils.string_equal(result_unit,"as",case_sensitive=case_sensitive):
        return value_s*1E18
    else:
        raise IOError("unrecognized length unit: {0}".format(result_unit))
        
def convert_frequency_units(value, value_unit="Hz", result_unit="Hz", case_sensitive=True):
    """
    Convert `value` from `value_unit` to `result_unit`.
    
    The possible frequency units are ``'Hz'``,``'kHz'``, ``'MHz'``, ``'GHz'``.
    If ``case_sensitive==True``, matching units is case sensitive. 
    """
    if string_utils.string_equal(value_unit,"Hz",case_sensitive=case_sensitive):
        value_Hz=value
    elif string_utils.string_equal(value_unit,"kHz",case_sensitive=case_sensitive):
        value_Hz=value*1E3
    elif string_utils.string_equal(value_unit,"MHz",case_sensitive=case_sensitive):
        value_Hz=value*1E6
    elif string_utils.string_equal(value_unit,"GHz",case_sensitive=case_sensitive):
        value_Hz=value*1E9
    else:
        raise IOError("unrecognized frequency unit: {0}".format(value_unit))
    if string_utils.string_equal(result_unit,"Hz",case_sensitive=case_sensitive):
        return value_Hz
    elif string_utils.string_equal(result_unit,"kHz",case_sensitive=case_sensitive):
        return value_Hz/1E3
    elif string_utils.string_equal(result_unit,"MHz",case_sensitive=case_sensitive):
        return value_Hz/1E6
    elif string_utils.string_equal(result_unit,"GHz",case_sensitive=case_sensitive):
        return value_Hz/1E9
    else:
        raise IOError("unrecognized frequency unit: {0}".format(result_unit))
        
def convert_power_units(value, value_unit="dBm", result_unit="dBm", case_sensitive=True, impedance=50.):
    """
    Convert `value` from `value_unit` to `result_unit`.
    
    For conversion between voltage and power, assume RMS voltage and the given `impedance`.
    The possible power units are ``'dBm'``, ``'dBmV'``, ``'dBuV'``, ``'W'``, ``'mW'``, ``'uW'``, ``'nW'``, ``'mV'``, ``'nV'``.
    If ``case_sensitive==True``, matching units is case sensitive. 
    """
    # dBmV=20*log10(V/1mV), 220mV<->1mW => 20*log10(220)dBmV=47dBmV<->0dBm
    s=1.
    W2V_dB=np.log10(impedance)*10.
    if string_utils.string_equal(value_unit,"dBm",case_sensitive=case_sensitive):
        value_dBm=value
    elif string_utils.string_equal(value_unit,"dBmV",case_sensitive=case_sensitive):
        value_dBm=value-30.-W2V_dB
    elif string_utils.string_equal(value_unit,"dBuV",case_sensitive=case_sensitive):
        value_dBm=value-90.-W2V_dB
    else:
        s=np.sign(value)
        value=abs(value)
        if string_utils.string_equal(value_unit,"W",case_sensitive=case_sensitive):
            value_dBm=10.*np.log10(value)+30.
        elif string_utils.string_equal(value_unit,"mW",case_sensitive=case_sensitive):
            value_dBm=10.*np.log10(value)
        elif string_utils.string_equal(value_unit,"uW",case_sensitive=case_sensitive):
            value_dBm=10.*np.log10(value)-30.
        elif string_utils.string_equal(value_unit,"nW",case_sensitive=case_sensitive):
            value_dBm=10.*np.log10(value)-60.
        elif string_utils.string_equal(value_unit,"mV",case_sensitive=case_sensitive):
            value_dBm=20.*np.log10(value)-30.-W2V_dB
        elif string_utils.string_equal(value_unit,"uV",case_sensitive=case_sensitive):
            value_dBm=20.*np.log10(value)-90.-W2V_dB
        else:
            raise IOError("unrecognized power unit: {0}".format(value_unit))
    if string_utils.string_equal(result_unit,"dBm",case_sensitive=case_sensitive):
        return value_dBm if s>0 else np.nan
    elif string_utils.string_equal(result_unit,"dBmV",case_sensitive=case_sensitive):
        return value_dBm+30.+W2V_dB if s>0 else np.nan
    elif string_utils.string_equal(result_unit,"dBuV",case_sensitive=case_sensitive):
        return value_dBm+90.+W2V_dB if s>0 else np.nan
    elif string_utils.string_equal(result_unit,"W",case_sensitive=case_sensitive):
        return 10.**((value_dBm-30.)/10.)*s
    elif string_utils.string_equal(result_unit,"mW",case_sensitive=case_sensitive):
        return 10.**(value_dBm/10.)*s
    elif string_utils.string_equal(result_unit,"uW",case_sensitive=case_sensitive):
        return 10.**((value_dBm+30.)/10.)*s
    elif string_utils.string_equal(result_unit,"nW",case_sensitive=case_sensitive):
        return 10.**((value_dBm+60.)/10.)*s
    elif string_utils.string_equal(result_unit,"mV",case_sensitive=case_sensitive):
        return 10.**((value_dBm+30.+W2V_dB)/20.) if s>0 else np.nan
    elif string_utils.string_equal(result_unit,"uV",case_sensitive=case_sensitive):
        return 10.**((value_dBm+90.+W2V_dB)/20.) if s>0 else np.nan
    else:
        raise IOError("unrecognized power unit: {0}".format(result_unit))