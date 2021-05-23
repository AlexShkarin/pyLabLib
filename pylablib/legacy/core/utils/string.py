"""
String search, manipulation and conversion routines.
"""
from future.utils import viewvalues
from .py3 import textstring, as_builtin_bytes, as_str

from . import funcargparse

import re
import fnmatch
import struct
import collections

import numpy as np


##### Searching and equality #####

def string_equal(name1, name2, case_sensitive=True, as_prefix=False):
    """
    Determine if `name1` and `name2` are equal with taking special rules (`case_sensitive` and `as_prefix`) into account.
    
    If ``as_prefix==True``, strings match even if `name1` is just a prefix of `name2`.
    """
    if not case_sensitive:
        name1=name1.lower()
        name2=name2.lower()
    if as_prefix:
        return name2.startswith(name1)
    else:
        return name2==name1
    
def find_list_string(name, str_list, case_sensitive=True, as_prefix=False, first_matched=False):
    """
    Find `name` in the string list.
    
    Comparison parameters are defined in :func:`string_equal`.
    If ``first_matched==True``, stop at the first match; otherwise if multiple occurrences happen, raise :exc:`ValueError`.
    
    Returns:
        tuple ``(index, value)``.
    """
    if not case_sensitive:
        lookup_name=name.lower()
    else:
        lookup_name=name
    found_name=None
    for i,s in enumerate(str_list):
        if not case_sensitive:
            lookup_s=s.lower()
        else:
            lookup_s=s
        if as_prefix:
            sat=lookup_s.startswith(lookup_name)
        else:
            sat=(lookup_s==lookup_name)
        if sat:
            if found_name is None:
                found_name=(i,s)
                if first_matched:
                    break
            else:
                raise ValueError("{0} and {1} both satisfy name {2}".format(found_name[1],s,name))
    if found_name is None:
        raise KeyError("can't find name in the container: {0}".format(name))
    return found_name
    
def find_dict_string(name, str_dict, case_sensitive=True, as_prefix=False):
    """
    Find name in the string list.
    
    Comparison parameters are defined in :func:`string_equal`. If multiple occurrences happen, raise :exc:`ValueError`.
    
    Returns:
        tuple ``(key, value)``.
    """
    if case_sensitive and not as_prefix:
        try:
            return name, str_dict[name]
        except KeyError:
            raise KeyError("can't find name in the container: {0}".format(name))
    found_name=find_list_string(name,str_dict,case_sensitive=case_sensitive,as_prefix=as_prefix)[1]
    return found_name, str_dict[found_name]


def find_first_entry(line, elements, start=0, not_found_value=-1):
    """
    Find the index of the earliest position inside the `line` of any of the strings in `elements`, starting from `start`.
    
    If none are found, return `not_found_value`.
    """
    first_entry=len(line)
    for e in elements:
        pos=line.find(e,start)
        if pos>0:
            first_entry=min(first_entry,pos)
    if first_entry==len(line):
        return not_found_value
    return first_entry


##### String filter #####

def translate_string_filter(filt, syntax, match_case=True, default=False):
    """
    Turns `filt` into a matching function.
    
    The matching function takes single :class:`str` argument, returns :class:`bool` value.
    
    `filt` can be
        - ``None``: function always returns default,
        - :class:`bool`: function always returns this value,
        - :class:`str`: pattern, determined by `syntax`,
        - anything else: returned as is (assumed to already be a callable).
    
    `syntax` can be ``'re'`` (:mod:`re`), ``'glob'`` (:mod:`glob`) or ``'pred'`` (simply matching predicate).
    `match_case` determines whether the filter cares about the string case when matching.
    """
    if filt is None:
        return lambda _: default
    if isinstance(filt, bool):
        return lambda _: filt
    funcargparse.check_parameter_range(syntax,"syntax",{"re","glob","pred"})
    if syntax=="re":
        comp=re.compile(filt,flags=0 if match_case else re.IGNORECASE)
        return lambda x: (comp.match(x) is not None)
    elif syntax=="glob":
        comp=re.compile(fnmatch.translate(filt))
        return lambda x: (comp.match(x) is not None)
    else:
        return filt

class StringFilter(object):
    """
    String filter function.
    
    Matches string if it matches include (matches all strings by default) and doesn't match exclude (matches nothing by default).
    
    Args:
        include: Inclusion filter (translated by :func:`translate_string_filter`; regex by default).
        exclude: Exclusion filter (translated by :func:`translate_string_filter`; regex by default).
        syntax: Default syntax for pattern filters.
        match_case (bool): Determines whether filter ignores case when matching.
    """
    def __init__(self, include=None, exclude=None, syntax="re", match_case=False):
        object.__init__(self)
        self.include=translate_string_filter(include,syntax,match_case=match_case,default=True)
        self.exclude=translate_string_filter(exclude,syntax,match_case=match_case,default=False)
    def __call__(self, s):
        return self.include(s) and not self.exclude(s)
def get_string_filter(include=None, exclude=None, syntax="re", match_case=False):
    """
    Generate :class:`StringFilter` with the given parameters.
    
    If the first argument is already :class:`StringFilter`, return as is. If it's a tuple, expand as argument list.
    """
    if isinstance(include, StringFilter):
        return include
    if isinstance(include, tuple):
        return StringFilter(*include)
    return StringFilter(include,exclude,syntax=syntax,match_case=match_case)
def sfglob(include=None, exclude=None):
    """
    Return string filter based on :mod:`glob` syntax.
    """
    return get_string_filter(include=include,exclude=exclude,syntax="glob")
def sfregex(include=None, exclude=None, match_case=False):
    """
    Return string filter based on :mod:`re` syntax.
    """
    return get_string_filter(include=include,exclude=exclude,syntax="re",match_case=match_case)
def filter_string_list(l, filt):
    """
    Filter string list based on the filter.
    """
    if filt is None:
        return l
    else:
        filt=get_string_filter(filt)
        return [f for f in l if filt(f)]




##### Conversion routines #####

class _EmptyString(object):
    """
    Dummy object to represent an empty string for conversion purposes.
    """
    def __init__(self):
        object.__init__(self)
    def __str__(self):
        return ""
    def __repr__(self):
        return "empty_string"
empty_string=_EmptyString()



_hard_delimiters="\n\t\v\r"
_soft_delimiters=" ,"
_quotation_characters="\"'"

_to_escape=_hard_delimiters+_quotation_characters
_escape_special_rules={"\n":"n","\t":"t","\v":"v","\r":"r"}
_unescape_special_rules=dict([(v,k) for (k,v) in _escape_special_rules.items()])

_parenthesis_pairs={"(":")", "[":"]", "{":"}"}



_border_escaped=_quotation_characters+" "
def escape_string(value, location="element", quote_type='"'):
    """
    Escape string.
    
    Escaping can be partially skipped depending on `location`:
        - ``"parameter"``: escape only if it contains hard delimiters (``"\\n\\t\\v\\r"``) anywhere
            or _border_escaped (``"``, ``'`` or space) on the sides (suited for parameters taking the full string);
        - ``"entry"``: same as above, plus containing soft delimiters anywhere (suited for entries of a table);
        - ``"element"``: always escaped
    
    If `quote_type` is not ``None``, automatically put the string into the specified quotation marks;
        if `quote_type` is ``None``, all quotation marks are escaped; if it's not ``None``, only `quote_type` marks are escaped.
    """
    funcargparse.check_parameter_range(location,"location",{"element","entry","parameter"})
    process=False
    if location=="element":
        process=True
    if location in ["parameter","entry"]:
        if len(value)==0 or (value[0] in _border_escaped) or (value[-1] in _border_escaped):
            process=True
        for c in _hard_delimiters:
            if value.find(c)>=0:
                process=True
    if location=="entry":
        for c in _soft_delimiters:
            if value.find(c)>=0:
                process=True
    if process:
        value=value.replace("\\","\\\\")
        for c in _to_escape:
            if (quote_type is not None) and (c in _quotation_characters) and (c!=quote_type):
                continue
            r="\\"+_escape_special_rules.get(c,c)
            value=value.replace(c,r)
        if quote_type is not None:
            value=quote_type+value+quote_type
    return value

def _numpy_to_str(a, custom_representations=None):
    """Convert multidimensional numpy array into a string using the standard number representation rules"""
    if a.ndim==0:
        return to_string(a,custom_representations=custom_representations,use_classes=True)
    elif a.ndim==1:
        return to_string(list(a),custom_representations=custom_representations,use_classes=True)
    else:
        return "["+", ".join([_numpy_to_str(e,custom_representations=custom_representations) for e in a])+"]"

_default_float_representation="{:.12E}"
_default_complex_representation="{:.12E}"
_default_int_representation="{:d}"
TConversionClass=collections.namedtuple("TConversionClass",["label","cls","to_str","from_str"])
_conversion_classes=[("array",np.ndarray,_numpy_to_str,np.array)]
def to_string(value, location="element", custom_representations=None, parenthesis_rules="text", use_classes=False):
    """
    Convert value to string with an option of modifying format string.
    
    Args:
        value
        location (str): Used for converting strings (see :func:`escape_string`).
        custom_representations (dict): dictionary ``{value_type: fmt}``,
            where value type can be ``'int'``, ``'float'`` or ``'complex'`` and `fmt` is a :meth:`str.format` string.
        parenthesis_rules (str): determine how to deal with single-element tuples and complex numbers
            can be ``"text"`` (single-element tuples are represented with simple parentheses, e.g., ``"(1)"``; complex number are represented without parentheses, e.g., ``"1+2j"``)
            or ``"python"`` (single-element tuples are represented with a comma in the end, e.g., ``"(1,)"``; complex number are represented with parentheses, e.g., ``"(1+2j)"``)
        use_classes (bool): if ``True``, use additional representation classes for special objects
            (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``).
            This improves conversion fidelity, but makes result harder to parse (e.g., by external string parsers).
    """
    funcargparse.check_parameter_range(parenthesis_rules,"parenthesis_rules",{"text","python"})
    kwargs={"custom_representations":custom_representations,"parenthesis_rules":parenthesis_rules,"use_classes":use_classes}
    tr=custom_representations or {}
    if isinstance(value,complex):
        val=tr.get("complex",_default_complex_representation).format(complex(value))
        return val if parenthesis_rules=="text" else "("+val+")"
    if isinstance(value,float) or isinstance(value,np.floating):
        return tr.get("float",_default_float_representation).format(float(value))
    if isinstance(value,bool):
        return str(value)
    if isinstance(value,int) or isinstance(value,np.long) or isinstance(value,np.integer):
        return tr.get("int",_default_int_representation).format(int(value))
    if isinstance(value,textstring):
        return escape_string(value, location=location)
    if isinstance(value,list):
        return "["+", ".join(to_string(e,location="element",**kwargs) for e in value)+"]"
    if isinstance(value, tuple):
        val="("+", ".join(to_string(e,location="element",**kwargs) for e in value)+")"
        return val if parenthesis_rules=="text" else val[:-1]+",)"
    if isinstance(value, set):
        return "{"+", ".join(to_string(e,location="element",**kwargs) for e in value)+"}"
    if isinstance(value, dict):
        return "{"+", ".join("{}: {}".format(
                to_string(k,location="element",**kwargs),
                to_string(v,location="element",**kwargs))
                            for k,v in value.items())+"}"
    if isinstance(value,np.ndarray) and not use_classes:
        if np.ndim(value)==0:
            return to_string(np.asscalar(value),**kwargs)
        return to_string(list(value),**kwargs)
    if use_classes:
        for label,cls,to_str,_ in _conversion_classes:
            if isinstance(value,cls):
                return "{}({})".format(label,to_str(value,custom_representations=custom_representations))
    value=str(value) # booleans and None are included here
    for ec in "\n\v\r":
        value=value.replace(ec,"\t")
    return value
_conv_types=[float,int,np.floating,np.integer,textstring,complex,np.long,bool]
_cont_types=[list,tuple,set]
def is_convertible(value):
    """
    Check if the value can be converted to a string using standard :func:`to_string` function.
    """
    for t in _conv_types:
        if isinstance(value,t):
            return True
    for t in _cont_types:
        if isinstance(value,t):
            return all(is_convertible(v) for v in value)
    if isinstance(value,dict):
        return all(is_convertible(v) for v in viewvalues(value)) and all(is_convertible(v) for v in value) 
    if isinstance(value,np.ndarray) and np.ndim(value)<2:
        return True
    return (value is None)




def _extract_digits(s, start=0, maxlen=None):
    end=start
    while end<len(s) and (maxlen is None or start+maxlen>end) and s[end].isdigit():
        end=end+1
    return s[start:end]

def extract_escaped_string(line, start=0):
    """
    Extract escaped string in quotation marks from the `line`, starting from `start`.
    
    ``line[start]`` should be a quotation mark (``'`` or ``"``) or ``b`` followed by a quotation mark (for binary strings).
    
    Returns:
        tuple ``(end position, un-escaped string)``.
    """
    if start==len(line):
        return start,""
    if start>len(line):
        raise ValueError("starting position is further than line length")
    if line[start].lower()=="b":
        binary=True
        start+=1
    else:
        binary=False
    start_quote=line[start]
    if not (start_quote in _quotation_characters):
        raise ValueError("malformatted string representation")
    pos=start+1
    unescaped=""
    while True:
        quote_lookup=line.find(start_quote,pos)
        if quote_lookup<0:
            raise ValueError("malformatted string representation")
        dash_lookup=line.find("\\",pos)
        if dash_lookup<0 or quote_lookup<dash_lookup:
            unescaped=unescaped+line[pos:quote_lookup]
            return quote_lookup+1,(as_builtin_bytes(unescaped) if binary else unescaped)
        if dash_lookup==len(line)-1:
            raise ValueError("malformatted string representation")
        escaped_character=line[dash_lookup+1]
        if escaped_character=='x': #\x00
            hexn=_extract_digits(line,dash_lookup+2,2)
            if hexn=="":
                raise ValueError("malformatted string representation")
            escaped_character=as_str(struct.pack("B",int(hexn,16)))
            next_pos=dash_lookup+2+len(hexn)
        elif escaped_character.isdigit(): #\000
            octn=_extract_digits(line,dash_lookup+1,3)
            escaped_character=as_str(struct.pack("B",int(octn,8)))
            next_pos=dash_lookup+1+len(octn)
        else:
            escaped_character=_unescape_special_rules.get(escaped_character,escaped_character)
            next_pos=dash_lookup+2
        unescaped=unescaped+line[pos:dash_lookup]+escaped_character
        pos=next_pos
def unescape_string(value):
    """
    Un-escape string.
    
    Assume that all quotation marks have been escaped. 
    """
    pos,unescaped=extract_escaped_string('"'+value+'"')
    if pos!=len(value):
        raise ValueError("malformatted string representation")
    return unescaped

def _parse_parenthesis_struct(line, start=0, use_classes=True):
    """
    Parse parenthesis structure from the line, starting from start.
    
    Takes string constants into account.
    """
    if start>=len(line) or not (line[start] in _parenthesis_pairs):
        raise ValueError("structure {0} is not well-formatted: non-paired parentheses".format(str))
    pos=start+1
    open_par=line[start]
    elts=[]
    curr_elt=None
    while True:
        quote_pos=find_first_entry(line,_quotation_characters,pos,len(line))
        delim_pos=find_first_entry(line,[',',':'],pos,len(line))
        open_par_pos=find_first_entry(line,_parenthesis_pairs,pos,len(line))
        clos_par_pos=find_first_entry(line,_parenthesis_pairs.values(),pos,len(line))
        if clos_par_pos==len(line):
            raise ValueError("malformatted parenthesis structure")
        min_pos=min(quote_pos,delim_pos,open_par_pos,clos_par_pos)
        if min_pos==quote_pos:
            gap=line[pos:min_pos]
            if len(gap)>0 and gap[-1].lower()=="b":
                min_pos-=1
                gap=gap[:-1]
            if len(gap)>0 and not gap.isspace():
                raise ValueError("malformatted parenthesis structure")
            if curr_elt is None:
                new_pos,escaped_string=extract_escaped_string(line,min_pos)
                curr_elt=("'",escaped_string)
                pos=new_pos
            else:
                raise ValueError("malformatted parenthesis structure")
        elif min_pos==open_par_pos:
            gap=line[pos:min_pos]
            label=None
            if len(gap)>0 and not gap.isspace():
                label=gap.lstrip()
                if not (use_classes and label in [cc[0] for cc in _conversion_classes]):
                    raise ValueError("malformatted parenthesis structure")
            if curr_elt is None:
                new_pos,parsed_substructure=_parse_parenthesis_struct(line,min_pos,use_classes=use_classes)
                if label is None:
                    curr_elt=(line[min_pos],parsed_substructure)
                else:
                    curr_elt=("e",line[pos:new_pos].strip())
                pos=new_pos
            else:
                raise ValueError("malformatted parenthesis structure")
        elif min_pos==delim_pos or min_pos==clos_par_pos:
            closing_token=line[min_pos]
            if min_pos==clos_par_pos and closing_token!=_parenthesis_pairs[open_par]:
                raise ValueError("malformatted parenthesis structure")
            if curr_elt is None:
                curr_elt=("e",line[pos:min_pos].strip())
            else:
                gap=line[pos:min_pos]
                if len(gap)>0 and not gap.isspace():
                    raise ValueError("malformatted parenthesis structure")
            elts.append(curr_elt+(closing_token,))
            curr_elt=None
            pos=min_pos+1
            if min_pos==clos_par_pos:
                return min_pos+1,elts
def to_range(range_tuple):
    def is_zero(e):
        return (not e) or (e is empty_string)
    range_tuple=[0 if is_zero(e) else e for e in range_tuple]
    return list(np.arange(*range_tuple))
def _convert_parenthesis_struct(struct, case_sensitive=True, parenthesis_rules="text"):
    """
    Covert parsed parenthesis structure into python objects.
    
    `parenthesis_rules` determine how to deal with empty entries (e.g., ``[1,,3]``) and complex number representation (``"1+2j"`` vs. ``"(1+2j)"``):
        - ``'text'``: any empty entries are translated into ``empty_string`` (i.e., ``[,] -> [empty_string, empty_string]``), except for completely empty structures (``[]`` or ``()``);
            complex numbers are represented without parentheses, so that ``"(1+2j)"`` will be interpreted as a single-element tuple ``(1+2j,)``.
        - ``'python'``: empty entries in the middle are not allowed; empty entries at the end are ignored (i.e., ``[2,] -> [2]``)
            (single-element tuple can still be expressed in two ways: ``(e,)`` or ``(e)``);
            complex numbers are by default represented with parentheses, so that ``"(1+2j)"`` will be interpreted as a complex number,
            and only ``(1+2j,)``, ``((1+2j))`` or ``((1+2j),)`` as a single-element tuple.
    """
    funcargparse.check_parameter_range(parenthesis_rules,"parenthesis_rules",{"text","python"})
    elt_type,elt_val,_=struct
    if elt_type=="e":
        return from_string(elt_val,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules)
    elif elt_type in _quotation_characters:
        return elt_val
    elif elt_type in _parenthesis_pairs:
        if parenthesis_rules=="python" and elt_type=="(" and len(elt_val)==1: # complex number check
            val=elt_val[0]
            if val[0]=="e" and _complex_re.match("("+val[1]+")"):
                strval=val[1]
                try:
                    return complex(strval)
                except ValueError:
                    pass
                try:
                    return complex(strval.lower().replace("i","j"))
                except ValueError:
                    pass
        if parenthesis_rules=="text":
            if (len(elt_val)==1) and (elt_val[0][:2]==("e","")):
                elt_val=[]
        elif parenthesis_rules=="python":
            if (len(elt_val)>0) and (elt_val[-1][:2]==("e","")):
                elt_val=elt_val[:-1]
            for e in elt_val:
                if e[:2]==("e",""):
                    raise ValueError("malformatted parenthesis structure")
        closing_tokens=[e[2] for e in elt_val]
        parsed=[_convert_parenthesis_struct(e,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules) for e in elt_val]
        if elt_type in "[(":
            if any([ct==":" for ct in closing_tokens]):
                #raise ValueError("malformatted parenthesis structure")
                expanded=[]
                curr_range=tuple()
                for e_val,e_ct in zip(parsed,closing_tokens):
                    if e_ct==":":
                        if len(curr_range)>1:
                            raise ValueError("malformatted parenthesis structure")
                        else:
                            curr_range=curr_range+(e_val,)
                    else:
                        if len(curr_range)==0:
                            expanded.append(e_val)
                        else:
                            curr_range=curr_range+(e_val,)
                            expanded=expanded+to_range(curr_range)
                            curr_range=tuple()
                parsed=expanded
            if elt_type=="(":
                parsed=tuple(parsed)
            return parsed
        elif elt_type=="{":
            if len(parsed)==0:
                return {}
            if all([ct=="," for ct in closing_tokens[:-1]]):
                return set(parsed)
            elif len(parsed)%2==0 and all([ct==":" for ct in closing_tokens[:-1:2]]) and all([ct=="," for ct in closing_tokens[1:-1:2]]):
                return dict(zip(parsed[::2],parsed[1::2]))
            else:
                raise ValueError("malformatted parenthesis structure")
    else:
        raise ValueError("unrecognized element type: {0}".format(elt_type))


_complex_re=re.compile(r"\(([\d.+-Ee]*[+-])?[\d.+-Ee]*[ij]\)|([\d.+-Ee]*[+-])?[\d.+-Ee]*[ij]")
def from_string(value, case_sensitive=True, parenthesis_rules="text", use_classes=True):
    """
    Parse a string.
    
    Recognizes integers, floats, complex numbers (with ``i`` or ``j`` for complex part), strings (in quotation marks), dicts, sets, list and tuples, booleans and ``None``.
    If item is unrecognizable, assumed to be a string.
    
    `case_sensitive` is applied when compared to ``None``, ``True`` or ``False``.
    
    `parenthesis_rules` determine how to deal with empty entries (e.g., ``[1,,3]``) and complex number representation (``"1+2j"`` vs. ``"(1+2j)"``):
        - ``'text'``: any empty entries are translated into ``empty_string`` (i.e., ``[,] -> [empty_string, empty_string]``), except for completely empty structures (``[]`` or ``()``);
            complex numbers are represented without parentheses, so that ``"(1+2j)"`` will be interpreted as a single-element tuple ``(1+2j,)``.
        - ``'python'``: empty entries in the middle are not allowed; empty entries at the end are ignored (i.e., ``[2,] -> [2]``)
            (single-element tuple can still be expressed in two ways: ``(e,)`` or ``(e)``);
            complex numbers are by default represented with parentheses, so that ``"(1+2j)"`` will be interpreted as a complex number,
            and only ``(1+2j,)``, ``((1+2j))`` or ``((1+2j),)`` as a single-element tuple.
    `use_classes`: if ``True``, try to find additional representation classes for special objects
        (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``).
    """
    value=value.strip()
    if len(value)==0:
        return empty_string
    if string_equal(value,"True",case_sensitive=case_sensitive):
        return True
    if string_equal(value,"False",case_sensitive=case_sensitive):
        return False
    if string_equal(value,"None",case_sensitive=case_sensitive):
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    if _complex_re.match(value):
        try:
            return complex(value)
        except ValueError:
            pass
        try:
            return complex(value.lower().replace("i","j"))
        except ValueError:
            pass
    if value[0] in _parenthesis_pairs:
        pos,parsed_value=_parse_parenthesis_struct(value,use_classes=use_classes)
        if pos==len(value): # malformatted parentheses structures are treated as strings
            struct=(value[0],parsed_value,None)
            return _convert_parenthesis_struct(struct,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules)
    if value[0] in _quotation_characters or (value[0].lower()=="b" and len(value)>1 and value[1] in _quotation_characters):
        pos,unescaped=extract_escaped_string(value)
        if pos!=len(value):
            raise ValueError("malformatted string representation")
        return unescaped
    if use_classes:
        for label,_,_,from_str in _conversion_classes:
            if value.startswith(label+"("):
                parsed=from_string(value[len(label):],case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules)
                if isinstance(parsed,tuple):
                    return from_str(*parsed)
    return value


_delimiters=r"\s*,\s*|\s+"
_delimiters_regexp=re.compile(_delimiters)
def from_string_partial(value, delimiters=_delimiters_regexp, case_sensitive=True, parenthesis_rules="text", use_classes=True, return_string=False):
    """
    Convert the first part of the supplied string (bounded by `delimiters`) into a value.
    
    `delimites` is a string or a regexp (default is ``"\\s*,\\s*|\\s+"``).
    
    If ``return_string==False``, return tuple ``(end position, converted value)``; else, return tuple ``(end position, value string)``.
    
    The rest of the parameters is the same as in :func:`from_string`.
    """
    if isinstance(delimiters,textstring):
        delimiters=re.compile(delimiters)
    value=value.strip()
    end=None
    if value[0] in _parenthesis_pairs:
        end,parsed_value=_parse_parenthesis_struct(value,use_classes=use_classes)
        if not return_string:
            struct=(value[0],parsed_value,None)
            res=_convert_parenthesis_struct(struct,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules)
    elif value[0] in _quotation_characters:
        end,res=extract_escaped_string(value)
    elif use_classes:
        for label,_,_,from_str in _conversion_classes:
            if value.startswith(label+"("):
                end,parsed=from_string_partial(value[len(label):],delimiters=delimiters,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules,use_classes=use_classes,return_string=return_string)
                if return_string:
                    if parsed.startswith("(") and parsed.endswith(")"):
                        end,res=end+len(label)+1,parsed
                else:
                    if isinstance(parsed,tuple):
                        end,res=end+len(label)+1,from_str(*parsed)
                        break
    if end is not None:
        if return_string:
            res=value[:end]
        m=delimiters.match(value[end:])
        if m is not None:
            end=end+m.end()
        return end,res
    else:
        m=delimiters.search(value)
        if m is None:
            del_pos=(len(value),len(value))
        else:
            del_pos=(m.start(),m.end())
        res=value[:del_pos[0]]
        if not return_string:
            res=from_string(res)
        return del_pos[1],res
        
def from_row_string(value, delimiters=_delimiters_regexp, case_sensitive=True, parenthesis_rules="text", use_classes=True, return_string=False):
    """
    Convert the row string into a list of values, separated by delimiters.
    
    If ``return_string==False``, return list of converted objects; otherwise, return list of unconverted strings.
    
    The rest of the parameters is the same as in :func:`from_string_partial`.
    """
    if isinstance(delimiters,textstring):
        delimiters=re.compile(delimiters)
    tokens=[]
    while value:
        pos,token=from_string_partial(value,delimiters=delimiters,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules,use_classes=use_classes,return_string=return_string)
        tokens.append(token)
        value=value[pos:]
    return tokens