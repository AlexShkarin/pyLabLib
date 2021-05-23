import math
import re


SI_prefixes={"Y":1E+24,
             "Z":1E+21,
             "E":1E+18,
             "P":1E+15,
             "T":1E+12,
             "G":1E+9,
             "M":1E+6,
             "k":1E+3,
             "h":1E+2,
             "da":1E+1,
             "":1E+0,
             "d":1E-1,
             "c":1E-2,
             "m":1E-3,
             "u":1E-6,
             "n":1E-9,
             "p":1E-12,
             "f":1E-15,
             "a":1E-18,
             "z":1E-21,
             "y":1E-24}
SI_prefixes_print=dict([ (int(math.log10(o)),p) for p,o in SI_prefixes.items() if int(round(math.log10(o)))%3==0 ])

_SI_prefix_re_str="({0})".format( "|".join(SI_prefixes.keys()) )
_SI_float_re=re.compile(r'^\s*([+-]?)(\d*)(\.?)(\d*)((?:[Ee][+-]?\d+)?){0}\s*$'.format(_SI_prefix_re_str))
def parse_float(s):
    """
    Parse string as a float, with metric prefixes recognition.

    Return tuple ``(sign, integer, dot, fractional, exponent, prefix)``, where each entry has structure ``(begin, end, text)``.
    Return ``None`` if string is unrecognizable.
    """
    m=re.match(_SI_float_re,s)
    if m==None:
        return None
    g=m.groups()
    if g[1]=="" and g[3]=="":
        return None
    return tuple([(b,e,t) for (b,e),t in zip(m.regs[1:],g)])
def pos_to_order(s,pos):
    """
    For a given string representation of a float and position in the string, get the decimal order for this position.

    Return ``None`` if string is un-parsable or position is out of range (not in mantissa section of the number). 
    """
    parsed_value=parse_float(s)
    if parsed_value==None:
        return None
    sign_position=parsed_value[0][1]
    exponent_order=0
    if parsed_value[4][2]!="":
        exponent_order=int(parsed_value[4][2][1:])
    prefix_order=int(round( math.log10(SI_prefixes[parsed_value[5][2]]) ))
    order=exponent_order+prefix_order
    if pos<=sign_position: #before the number
        affected_digit=max(len(parsed_value[1][2])-1,0)
    elif pos<=parsed_value[1][1]: #inside integer part
        affected_digit=parsed_value[1][1]-pos
    elif pos==parsed_value[2][1]: #right after the dot (if it's not there, then this condition is never true)
        affected_digit=-1
    elif pos<=parsed_value[3][1]: #inside fractional part
        affected_digit=parsed_value[3][0]-pos
    else:
        return None
    return order+affected_digit
def order_to_pos(s,order):
    """
    For a given string representation of float and decimal order, get the position in the string corresponding to this order.

    If order is out of range for a given representation, truncates to most/least significant digit position.
    Return ``None`` if string is un-parsable. 
    """
    parsed_value=parse_float(s)
    if parsed_value==None:
        return None
    exponent_order=0
    if parsed_value[4][2]!="":
        exponent_order=int(parsed_value[4][2][1:])
    prefix_order=int(round( math.log10(SI_prefixes[parsed_value[5][2]]) ))
    rel_order=order-(exponent_order+prefix_order)
    
    if rel_order>=0:
        if rel_order>=len(parsed_value[1][2]):
            pos=parsed_value[1][0]
        else:
            pos=parsed_value[1][1]-rel_order
    else:
        if (-rel_order)>=len(parsed_value[3][2]):
            pos=parsed_value[3][1]
        else:
            pos=parsed_value[3][0]+(-rel_order)
    return pos
    


def str_to_float(s):
    """
    Return float value of a string, with metric prefixes recognition.

    Raise ``ValueError`` if string is unrecognizable. 
    """
    if len(s)==0:
        raise ValueError()
    if len(s)>2 and s[-2:] in SI_prefixes:
        prefix=SI_prefixes[s[-2:]]
        s=s[:-2]
    elif s[-1:] in SI_prefixes:
        prefix=SI_prefixes[s[-1:]]
        s=s[:-1]
    else:
        prefix=1.
    return float(s)*prefix
def is_integer(n, tolerance=0.):
    """
    Check if `n` is less than `tolerance` away from the nearest integer.
    """
    return abs(n-round(n))<=tolerance
def float_to_str_SI(n, digits=9, trailing_zeros=False):
    """
    Represent float using SI metric prefixes.

    For orders ``>=27`` and ``<-24`` use usual scientific notation with order being multiple of 3.
    If ``trailing_zeros==True``, then digits define precision, rather than number significant digits
    """
    if n==0:
        if trailing_zeros:
            return "0."+"0"*digits
        else:
            return "0"
    order=int(math.floor(math.log10(abs(n))))
    order_SI=(order/3)*3
    n=n*10**(-order_SI)
    if order_SI in SI_prefixes_print:
        prefix=SI_prefixes_print[order_SI]
    else:
        prefix="E{0:+d}".format(order_SI)
    if trailing_zeros:
        nstr="{{:.{:d}F}}".format(digits).format(n)
    else:
        nstr="{{:.{:d}G}}".format(digits).format(n)
    return nstr+prefix


class FloatFormatter(object):
    """
    Floating point number formatter.

    Callable object with takes a number as an argument and returns is string representation.

    Args:
        output_format(str): can be ``"auto"`` (use standard Python conversion), ``"SI"`` (use SI prefixes if possible), or ``"sci"`` (scientific "E" notation).
        digits (int): if ``trailing_zeros==False``, determines the number of significant digits; otherwise, determines precision (number of digits after decimal point).
        add_trailing_zeros (bool): if ``True``, always show fixed number of digits after the decimal point, with zero padding if necessary.
        leading_zeros (bool): determines the minimal size of the integer part (before the decimal point) of the number; pads with zeros if necessary.
        explicit_sign (bool): if ``True``, always add explicit plus sign.
    """
    def __init__(self, output_format="auto", digits=9, add_trailing_zeros=True, leading_zeros=0, explicit_sign=False):
        "If trailing_zeros==True, then digits define precision, rather than number significant digits"
        object.__init__(self)
        if not output_format in ["auto", "SI", "sci"]:
            raise ValueError("unrecognized output format: {0}".format(output_format))
        self.output_format=output_format
        self.explicit_sign=explicit_sign
        #if not output_format in ["significant", "precision"]:
        #    raise ValueError("unrecognized precision type: {0}".format(precision_type))
        #self.precision_type=precision_type
        self.digits=digits
        self.add_trailing_zeros=add_trailing_zeros
        self.leading_zeros=leading_zeros
    def __call__(self, value):
        if self.output_format=="auto":
            if self.add_trailing_zeros:
                dig="{{:.{:d}F}}".format(self.digits).format(abs(value))
            else:
                dig="{{:.{:d}G}}".format(self.digits).format(abs(value))
        elif self.output_format=="sci":
            if self.add_trailing_zeros:                
                dig="{{:.0{:d}E}}".format(self.digits).format(abs(value))
            else:
                dig="{{:.{:d}E}}".format(self.digits).format(abs(value))
        else:
            dig=float_to_str_SI(abs(value),self.digits,self.add_trailing_zeros)
        int_part_len=dig.find(".")
        if int_part_len<0:
            int_part_len=len(dig)
        if self.leading_zeros>int_part_len:
            dig="0"*(self.leading_zeros-int_part_len)+dig
        if self.explicit_sign and value>=0:
            dig="+"+dig
        elif value<0:
            dig="-"+dig
        return dig
        
class IntegerFormatter(object):
    """
    Simple integer number formatter.

    Callable object with takes a number as an argument and returns is string representation.

    For more flexibility (e.g., adding leading zeros) it is possible to use :class:`FloatFormatter` with ``digits=0`` and ``add_trailing_zeros=True``.
    """
    def __init__(self):
        object.__init__(self)
    def __call__(self, value):
        return "{:d}".format(int(value))

def as_formatter(formatter):
    """
    Turn an object into a formatter.

    Can be a callable object (returned as is), a string (``"float"`` or ``"int"``),
    or a tuple starting with ``"float"`` which contains arguments to the :class:`FloatFormatter`.
    """
    if hasattr(formatter,"__call__"):
        return formatter
    if formatter=="float":
        return FloatFormatter()
    if formatter=="int":
        return IntegerFormatter()
    if isinstance(formatter,tuple):
        if formatter[0]=="float":
            return FloatFormatter(*formatter[1:])
    raise ValueError("unknown formatter: {}".format(formatter))