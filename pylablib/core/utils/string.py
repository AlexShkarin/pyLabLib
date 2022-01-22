"""
String search, manipulation and conversion routines.
"""
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
    
    If ``as_prefix==True``, strings match even if `name1` is just a prefix of `name2` (not the other wait around).

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
                raise ValueError("{0} and {1} both satisfy name {2}".format(found_name[1],s,name))  # pylint: disable=unsubscriptable-object
    if found_name is None:
        raise KeyError("can't find name in the container: {0}".format(name))
    return found_name
    
def find_dict_string(name, str_dict, case_sensitive=True, as_prefix=False):
    """
    Find name in the string dictionary.
    
    Comparison parameters are defined in :func:`string_equal`.
    If multiple occurrences happen, raise :exc:`ValueError`.
    
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

def find_all_first_locations(line, elements, start=0, not_found_value=-1, known_locations=None):
    """
    Find the indices of the earliest position inside the `line` of all of the strings in `elements`, starting from `start`.
    
    Return dict ``{element: pos}``, where ``pos`` is either position in the string, or `not_found_value` if no entries are present.
    `known_locations` can specify a dictionary of already known locations of some of the elements.
    In this case, only missing elements or elements located before `start` will be re-evaluated.
    """
    positions=dict(known_locations) if known_locations is not None else {}
    for e in elements:
        if e not in positions or positions[e]<start:
            pos=line.find(e,start)
            positions[e]=pos if pos>0 else not_found_value
    return positions





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

class StringFilter:
    """
    String filter function.
    
    Matches string if it matches include (matches all strings by default) and doesn't match exclude (matches nothing by default).
    
    Args:
        include: Inclusion filter (translated by :func:`translate_string_filter` with syntax specified by `syntax`); include all by default.
        exclude: Exclusion filter (translated by :func:`translate_string_filter` with syntax specified by `syntax`); exclude none by default.
        syntax: Default syntax for pattern filters. Can be ``'re'`` (:mod:`re`), ``'glob'`` (:mod:`glob`) or ``'pred'`` (simply matching predicate).
        match_case (bool): Determines whether filter ignores case when matching.
    """
    def __init__(self, include=None, exclude=None, syntax="re", match_case=False):
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
    """Return string filter based on :mod:`glob` syntax"""
    return get_string_filter(include=include,exclude=exclude,syntax="glob")
def sfregex(include=None, exclude=None, match_case=False):
    """Return string filter based on :mod:`re` syntax"""
    return get_string_filter(include=include,exclude=exclude,syntax="re",match_case=match_case)
def filter_string_list(l, filt):
    """Filter string list based on the filter"""
    if filt is None:
        return l
    else:
        filt=get_string_filter(filt)
        return [f for f in l if filt(f)]




##### Conversion routines #####

class _EmptyString:
    """
    Dummy object to represent an empty string for conversion purposes.
    """
    def __str__(self):
        return ""
    def __repr__(self):
        return "empty_string"
empty_string=_EmptyString()



_hard_delimiters="\n\t\v\r"
_soft_delimiters=" ,"
_quotation_characters="\"'"

_to_escape=_hard_delimiters+_quotation_characters
_escape_special_rules={"\a":"a","\b":"b","\f":"f","\n":"n","\t":"t","\v":"v","\r":"r","\\":"\\"}
_unescape_special_rules=dict([(v,k) for (k,v) in _escape_special_rules.items()])

_parenthesis_pairs={"(":")", "[":"]", "{":"}"}



_border_escaped=_quotation_characters+" "
def escape_string(value, location="element", escape_convertible=True, quote_type='"'):
    """
    Escape string.
    
    Escaping can be partially skipped depending on `location`:
        - ``"parameter"``: escape only if it contains hard delimiters (``"\\n\\t\\v\\r"``) anywhere
            or ``_border_escaped`` (``"``, ``'`` or space) on the sides (suited for parameters taking the full string);
        - ``"entry"``: same as above, plus containing soft delimiters (``,`` or space) anywhere (suited for entries of a table);
        - ``"element"``: always escaped
    If ``escape_convertible==True``, escape strings which can be misinterpreted as other values, such as ``"1"`` or ``"[]"``;
        otherwise, escape only strings which contain special characters.
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
        if escape_convertible and _is_convertible(value):
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

TConversionClass=collections.namedtuple("TConversionClass",["label","cls","rep","conv"])
_conversion_classes=[]
def add_conversion_class(label, cls, rep, conv):
    """
    Add a string conversion class.

    Some values (e.g., numpy arrays or named tuples) lose some of their associated information when converted into strings.
    With this function is possible to define custom conversion rules for such classes.

    Args:
        label(str): class label (e.g., ``"array"``)
        cls: class which is used to determine if the value should use this conversion functions (e.g., ``np.ndarray``)
        rep: function which takes a single argument (object of class `cls`) and returns its representations;
            can return a string or an object which is easier to convert to a string (e.g., a list or a tuple)
        conv: function which takes one or several arguments (converted values of the class representation) and returns the corresponding object;
            if `rep` returns a tuple, treat it as a list of several arguments, which are passed to `conv` separately;
            otherwise, `conv` gets a single argument which is the result of `rep`

    When converting to string, if an object of class `cls` is encountered, it is converted in a string ``label(str_rep)`` (e.g., ``"array([0, 1, 2])"``),
    where ``str_rep`` is the result of calling `rep` (if this result is a tuple, avoid double parentheses,
    e.g., if the result is a tuple ``(1, 2)``, the string becomes ``"label(1, 2)"`` instead of ``"label((1, 2))"``).
    When converting from string, the values inside the parentheses are passed as arguments to `conv` function to get the resulting value.
    """
    for c in _conversion_classes:
        if c.label==label or c.cls is cls:
            raise ValueError("specified conversion class already exists: {}".format(c))
    _conversion_classes.append(TConversionClass(label,cls,rep,conv))
def add_namedtuple_class(cls):
    """
    Add conversion class for a given named tuple class.

    For details, see :func:`add_conversion_class`.
    """
    add_conversion_class(cls.__name__,cls,tuple,cls)
add_conversion_class("array",np.ndarray,np.ndarray.tolist,np.array)

_default_formats={float:".12E",complex:".12E",int:"d"}
def to_string(value, location="element", value_formats=None, parenthesis_rules="text", use_classes=False):
    """
    Convert value to string with an option of modifying format string.
    
    Args:
        value
        location (str): Used for converting strings (see :func:`escape_string`).
        value_formats (dict): dictionary ``{value_type: fmt}``,
            where value type can be ``int``, ``float`` or ``complex`` and `fmt` is a format string used to represent value of this type (e.g., ``"5.3f"``);
            default formats are ``{float:".12E", complex:".12E", int:"d"}``.
        parenthesis_rules (str): determine how to deal with single-element tuples and complex numbers
            can be ``"text"`` (single-element tuples are represented with simple parentheses, e.g., ``"(1)"``; complex number are represented without parentheses, e.g., ``"1+2j"``)
            or ``"python"`` (single-element tuples are represented with a comma in the end, e.g., ``"(1,)"``; complex number are represented with parentheses, e.g., ``"(1+2j)"``)
        use_classes (bool): if ``True``, use additional representation classes for special objects
            (e.g., numpy arrays will be represented as ``"array([1, 2, 3])"`` instead of just ``"[1, 2, 3]"``).
            This improves conversion fidelity, but makes result harder to parse (e.g., by external string parsers).
            See :func:`add_conversion_class` for more explanation.
    """
    funcargparse.check_parameter_range(parenthesis_rules,"parenthesis_rules",{"text","python"})
    kwargs={"value_formats":value_formats,"parenthesis_rules":parenthesis_rules,"use_classes":use_classes}
    fmt=value_formats or {}
    if isinstance(value,complex):
        rep="{:"+fmt.get(complex,_default_formats[complex])+"}"
        val=rep.format(complex(value))
        return val if parenthesis_rules=="text" else "("+val+")"
    if isinstance(value,float) or isinstance(value,np.floating):
        rep="{:"+fmt.get(float,_default_formats[float])+"}"
        return rep.format(float(value))
    if isinstance(value,bool):
        return str(value)
    if isinstance(value,int) or isinstance(value,np.integer):
        rep="{:"+fmt.get(int,_default_formats[int])+"}"
        return rep.format(int(value))
    if isinstance(value,textstring):
        return escape_string(value, location=location)
    if isinstance(value,list):
        return "["+", ".join(to_string(e,location="element",**kwargs) for e in value)+"]"
    if isinstance(value, tuple) and not use_classes:
        val="("+", ".join(to_string(e,location="element",**kwargs) for e in value)+")"
        return val if parenthesis_rules=="text" or len(value)!=1 else val[:-1]+",)"
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
        for label,cls,rep,_ in _conversion_classes:
            if isinstance(value,cls):
                rvalue=rep(value)
                svalue=to_string(rvalue,location="element",**kwargs)
                if isinstance(rvalue,tuple):
                    svalue=svalue[1:-1]
                return "{}({})".format(label,svalue)
        if isinstance(value, tuple):
            val="("+", ".join(to_string(e,location="element",**kwargs) for e in value)+")"
            return val if parenthesis_rules=="text" or len(value)!=1 else val[:-1]+",)"
    value=str(value) # booleans and None are included here
    for ec in "\n\v\r":
        value=value.replace(ec,"\t")
    return value
_conv_types=[float,int,np.floating,np.integer,textstring,complex,bool]
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
        return all(is_convertible(v) for v in value.values()) and all(is_convertible(v) for v in value) 
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
    
    ``line[start]`` should be a quotation mark (``'`` or ``"``) or ``r`` or ``b`` followed by a quotation mark (for raw or binary strings).
    
    Returns:
        tuple ``(end position, un-escaped string)``.
    """
    if start==len(line):
        return start,""
    if start>len(line):
        raise ValueError("starting position is further than line length")
    quals=set()
    for _ in range(2):
        if len(line)>start and line[start].lower() in "rb" and line[start].lower() not in quals:
            quals.add(line[start])
            start+=1
    binary="b" in quals
    raw="r" in quals
    if len(line)<=start:  # empty line, or line containing only r and b
        raise ValueError("malformatted string representation")
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
        next_pos=None
        if not raw:
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
            elif escaped_character in _unescape_special_rules:
                escaped_character=_unescape_special_rules[escaped_character]
                next_pos=dash_lookup+2
            elif escaped_character in _quotation_characters:
                next_pos=dash_lookup+2
        if next_pos is None:
            escaped_character="\\"+escaped_character
            next_pos=dash_lookup+2
        unescaped=unescaped+line[pos:dash_lookup]+escaped_character
        pos=next_pos
def unescape_string(value):
    """
    Un-escape string.
    
    Only attempt if the string starts a quotation mark ``"`` or ``'``.
    Otherwise (including strings like ``'r""'`` or ``'b""'``), return the string as is.
    Raise an error if the string starts with a quotation mark, but does not correspond to a proper escaped string
    (e.g., ``'"abc`` or ``'"abc"def``).
    """
    if not (value.startswith('"') or value.startswith("'")):
        return value
    pos,unescaped=extract_escaped_string(value)
    if pos!=len(value):
        raise ValueError("malformatted string representation")
    return unescaped

def _parse_parenthesis_struct(line, start=0, use_classes=True, elements_locations=None):
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
    elements_locations=elements_locations or {}
    all_elements=list(_quotation_characters)+[',',':']+list(_parenthesis_pairs.keys())+list(_parenthesis_pairs.values())
    while True:
        elements_locations=find_all_first_locations(line,all_elements,start=pos,not_found_value=len(line),known_locations=elements_locations)
        quote_pos=min([elements_locations[c] for c in _quotation_characters])
        delim_pos=min([elements_locations[c] for c in [',',':']])
        open_par_pos=min([elements_locations[c] for c in _parenthesis_pairs.keys()])
        clos_par_pos=min([elements_locations[c] for c in _parenthesis_pairs.values()])
        if clos_par_pos==len(line):
            raise ValueError("malformatted parenthesis structure")
        min_pos=min(quote_pos,delim_pos,open_par_pos,clos_par_pos)
        if min_pos==quote_pos:
            gap=line[pos:min_pos].lower()
            quals=set()
            while len(gap)>0 and gap[-1] in "rb" and gap[-1] not in quals:
                min_pos-=1
                quals.add(gap[-1])
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
                new_pos,parsed_substructure=_parse_parenthesis_struct(line,min_pos,use_classes=use_classes,elements_locations=elements_locations)
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
def _convert_parenthesis_struct(pstruct, case_sensitive=True, parenthesis_rules="text"):
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
    elt_type,elt_val,_=pstruct
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
            if len(elt_val)==1 and (elt_val[-1][:2]==("e","")): # parsing (,) into an empty tuple
                elt_val=elt_val[:-1]
            for e in elt_val:
                if e[:2]==("e",""):
                    raise ValueError("malformatted parenthesis structure")
        closing_tokens=[e[2] for e in elt_val]
        parsed=[_convert_parenthesis_struct(e,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules) for e in elt_val]
        if elt_type in "[(":
            if any([ct==":" for ct in closing_tokens]):
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
def _is_string_repr(s):
    quals=set()
    p=0
    while p<len(s):
        c=s[p].lower()
        if c in _quotation_characters:
            return True
        if c in "rb" and c not in quals:
            quals.add(c)
            p+=1
        else:
            return False
    return False

_complex_re=re.compile(r"\(([\d.+-Ee]*[+-])?[\d.+-Ee]*[ij]\)|([\d.+-Ee]*[+-])?[\d.+-Ee]*[ij]")
def from_string(value, case_sensitive=True, parenthesis_rules="text", use_classes=True):
    """
    Parse a string.
    
    Recognizes integers, floats, complex numbers (with ``i`` or ``j`` for complex part), strings (in quotation marks), dicts, sets, list and tuples, booleans and ``None``.
    If item is unrecognizable, assumed to be a string.
    
    Args:
        case_sensitive (bool): applied when compared to ``None``, ``True`` or ``False``.
        parenthesis_rules (str): determines how to deal with empty entries (e.g., ``[1,,3]``)
            and complex number representation (``"1+2j"`` vs. ``"(1+2j)"``):
            
                - ``'text'``: any empty entries are translated into ``empty_string`` (i.e., ``[,] -> [empty_string, empty_string]``),
                  except for completely empty structures (``[]`` or ``()``);
                  complex numbers are represented without parentheses, so that ``"(1+2j)"`` will be interpreted as a single-element tuple ``(1+2j,)``.
                - ``'python'``: empty entries in the middle are not allowed; empty entries at the end are ignored (i.e., ``[2,] -> [2]``)
                  (single-element tuple can still be expressed in two ways: ``(e,)`` or ``(e)``);
                  complex numbers are by default represented with parentheses, so that ``"(1+2j)"`` will be interpreted as a complex number,
                  and only ``(1+2j,)``, ``((1+2j))`` or ``((1+2j),)`` as a single-element tuple.
        use_classes (bool): if ``True``, use additional representation classes for special objects
            (e.g., ``"array([1, 2, 3])"`` will be converted into a numpy array instead of raising an error).
            See :func:`add_conversion_class` for more explanation.
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
    if _complex_re.match(value) and not (parenthesis_rules=="text" and value[0]=="("):
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
            pstruct=(value[0],parsed_value,None)
            return _convert_parenthesis_struct(pstruct,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules)
    if _is_string_repr(value):
        pos,unescaped=extract_escaped_string(value)
        if pos!=len(value):
            raise ValueError("malformatted string representation")
        return unescaped
    if use_classes:
        for label,_,_,conv in _conversion_classes:
            if value.startswith(label+"("):
                parsed=from_string(value[len(label):],case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules)
                if isinstance(parsed,tuple):
                    return conv(*parsed)
    return value
_like_number_re=re.compile(r"^[\d+-eij.]*$")
def _is_convertible(value):
    """Check if the string can be converted into a non-string value"""
    value=value.strip()
    if len(value)==0:
        return True
    value=value.lower()
    if value in ["true","false","none"]:
        return True
    if value[0] in _parenthesis_pairs or _is_string_repr(value):
        return True
    if _like_number_re.match(value):
        cvalue=value.replace("i","j")
        for cls in [int,float,complex]:
            try:
                cls(cvalue)
                return True
            except ValueError:
                pass
    for cc in _conversion_classes:
        if value.startswith(cc[0]+"("):
            return True
    return False


_delimiters=r"\s*,\s*|\s+"
_delimiters_regexp=re.compile(_delimiters)
def from_string_partial(value, delimiters=_delimiters_regexp, case_sensitive=True, parenthesis_rules="text", use_classes=True, return_string=False):
    """
    Convert the first part of the supplied string (bounded by `delimiters`) into a value.
    
    `delimiters` is a string or a regexp (default is ``"\\s*,\\s*|\\s+"``, i.e., comma or spaces).
    If ``return_string==False``, convert the value string and return tuple ``(end_position, converted_value)``; otherwise, return tuple ``(end_position, value_string)``.
    
    The rest of the parameters is the same as in :func:`from_string`.
    """
    if isinstance(delimiters,textstring):
        delimiters=re.compile(delimiters)
    value=value.strip()
    end=None
    if value[0] in _parenthesis_pairs:
        end,parsed_value=_parse_parenthesis_struct(value,use_classes=use_classes)
        if not return_string:
            pstruct=(value[0],parsed_value,None)
            res=_convert_parenthesis_struct(pstruct,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules)
    elif value[0] in _quotation_characters:
        end,res=extract_escaped_string(value)
    elif use_classes:
        for label,_,_,conv in _conversion_classes:
            if value.startswith(label+"("):
                end,parsed=from_string_partial(value[len(label):],delimiters=delimiters,case_sensitive=case_sensitive,parenthesis_rules=parenthesis_rules,use_classes=use_classes,return_string=return_string)
                if return_string:
                    if parsed.startswith("(") and parsed.endswith(")"):
                        end,res=end+len(label)+1,parsed
                else:
                    if isinstance(parsed,tuple):
                        end,res=end+len(label)+1,conv(*parsed)
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