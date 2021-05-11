"""
Miscellaneous utilities for reading data files.
"""

from . import parse_csv
from ..utils import dictionary, string

import datetime
import re


##### File type detection #####

def is_unprintable_character(chn):
    return chn<8 or 13<chn<27 or 27<chn<32
def detect_binary_file(stream):
    """Check if the opened file is binary"""
    pos=stream.tell()
    chunk=bytes(stream.read(4096))
    stream.seek(pos)
    for c in chunk:
        if is_unprintable_character(c):
            return True
    return False

_dict_line_soft=r"^[\S]*(/[\S]*)*\s+"
_dict_line_soft_regexp=re.compile(_dict_line_soft)
_dict_line_hard=r"^[\w]*(/[\w]*)+\s+"
_dict_line_hard_regexp=re.compile(_dict_line_hard)
_dicttable_line=r"^#+\s*table\s+(start|end)"
_dicttable_line_regexp=re.compile(_dicttable_line)
def test_row_type(line):
    """
    Try to determine whether the line is a comment line, a numerical data row, a dictionary row or an unrecognized row.
    
    Doesn't distinguish with a great accuracy; useful only for trying to guess file format. 
    """
    line=line.strip().lower()
    if line=="":
        return "empty"
    if _dicttable_line_regexp.match(line):
        return "dict_table"
    if line[0]=="#":
        return "comment"
    if _dict_line_hard_regexp.match(line):
        return "dict"
    split_line=parse_csv._table_delimiters_regexp.split(line)
    split_line=[el for el in split_line if el!=""]
    try:
        for e in split_line:
            if not e in {"","nan",'inf',"+inf","-inf"}:
                complex(e.replace("i","j"))
        return "numerical"
    except ValueError:
        return "unrecognized"
def detect_textfile_type(stream):
    """Try to autodetect text file type: dictionary or table"""
    line_type_count={"empty":0,"dict":0,"dict_table":0,"comment":0,"numerical":0,"unrecognized":0}
    pos=stream.tell()
    data_lines=0
    while data_lines<20:
        l=stream.readline()
        if l=="":
            break
        line_type=test_row_type(l)
        line_type_count[line_type]=line_type_count[line_type]+1
        if line_type in {"dict","numerical"}:
            data_lines=data_lines+1
    stream.seek(pos)
    if line_type_count["dict_table"]>0 and data_lines>2:
        return "dict"
    if data_lines<5 and data_lines<line_type_count["unrecognized"]*2:
        return "unrecognized"
    if line_type_count["dict"]>line_type_count["numerical"]:
        return "dict"
    else:
        return "table"
    
_time_expr=r"(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s+(\d+)\s*:\s*(\d+)\s*:\s*(\d+)(.\d+)?"
_time_comment=r"(?:saved|created)\s+(?:on|at)\s*"+_time_expr
_time_comment_regexp=re.compile(_time_comment,re.IGNORECASE)
def test_savetime_comment(line):
    """Test if the comment resembles a savetime line"""
    m=_time_comment_regexp.match(line)
    if m is None:
        return None
    else:
        year,month,day,hour,minute,second,usec=m.groups()
        usec=usec or 0
        return datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second),int(float(usec)*1E6))
def find_savetime_comment(comments):
    """Try to find savetime comment"""
    if len(comments)==0:
        return None
    i=0
    for i,c in enumerate(comments):
        creation_time=test_savetime_comment(c)
        if creation_time is not None:
            break
    if i<len(comments):
        del comments[i]
    return creation_time
def test_columns_line(line, cols_num):
    """Test if the line looks like a list of columns for a given columns number"""
    split_line=string.from_row_string(line,parse_csv._table_delimiters_regexp)
    if len(split_line)!=cols_num:
        return None
    try:
        for e in split_line:
            complex(e.replace("i","j"))
        return None # all numerical, can't be column names
    except (ValueError, AttributeError):
        return split_line
def find_columns_lines(corrupted, comments, cols_num):
    """Try to find a column line (for a given columns number) among the comment and corrupted lines"""
    if len(corrupted["type"])>0:
        return corrupted["type"][0],None
    for i,l in enumerate(comments):
        columns=test_columns_line(l,cols_num)
        if columns is not None:
            return columns,i
    return None,None



class InlineTable:
    """Simple marker class that denotes that the wrapped numpy 2D array should be written inline"""
    def __init__(self, table):
        self.table=table
    def __repr__(self):
        return "InlineTable({})".format(self.table)

def parse_dict_line(line):
    """Parse stripped dictionary file line"""
    if not line:
        return None
    try:
        vpos,key=string.from_string_partial(line,delimiters=r"\s+",return_string=True)
    except ValueError:  # assume not-value line
        return (line,)
    try:
        key=string.unescape_string(key)
    except ValueError:  # leave the key as is
        pass
    if vpos==len(line):
        return (key,)
    else:
        value=string.from_string(line[vpos:].strip())
        return key,value

_dicttable_start=r"^#+\s*(table\s+(start|begin)|(start|begin)\s+table|table)"
_dicttable_start_regexp=re.compile(_dicttable_start,re.IGNORECASE)
_dicttable_end=r"^#+\s*(table\s+(end|finish)|(end|finish)\s+table|end)[\s#]*$"
_dicttable_end_regexp=re.compile(_dicttable_end,re.IGNORECASE)
def read_dict_and_comments(f, case_normalization=None, inline_dtype="generic", allow_duplicate_keys=False):
    """
    Load dictionary entries and comments from the file stream.

    Args:
        f: file stream
        case_normalization: case normalization for the returned dictionary; ``None`` means that it's case sensitive, ``"upper"`` and ``"lower"`` determine how they are normalized
        inline_dtype: dtype for inline tables; by default, use the most generic type (can include Python objects such as lists or strings)
        allow_duplicate_keys: if ``False`` and the same key is listed twice, raise and error

    Return tuple ``(data, comment_lines)``, where ``data`` is a dictionary with parsed entries (tables are still represented as 'raw', i.e., as a tuple of columns list and column names list),
    and ``comment_lines`` is a list of comment lines
    """
    data=dictionary.Dictionary(case_normalization=case_normalization)
    comment_lines=[]
    line=f.readline()
    root_keys=[]
    prev_key=None
    while line:
        line=line.strip()
        if line!="":
            if line[:1]!='#': #dict row
                if line.startswith("///"): # root key one level up
                    root_keys=root_keys[:-1]
                elif line.startswith("//"): # new nested root key
                    root_keys.append(line[2:])
                else:
                    parsed=parse_dict_line(line)
                    if parsed is not None:
                        if len(parsed)==1:
                            key=parsed[0]
                            if root_keys:
                                key="/".join(root_keys)+"/"+key
                            prev_key=(key,) # single-key line possibly means that an inline table follows
                        else:
                            key,value=parsed
                            if root_keys:
                                key="/".join(root_keys)+"/"+key
                            if not allow_duplicate_keys and key in data:
                                raise IOError("entry {} is already present in the dictionary".format(key))
                            data[key]=value
                            prev_key=key
            else:
                if _dicttable_start_regexp.match(line[1:]) is not None:
                    table,comments,corrupted=parse_csv.read_table(f,dtype=inline_dtype,stop_comment=_dicttable_end_regexp)
                    columns,comment_idx=find_columns_lines(corrupted,comments,len(table[0]))
                    if comment_idx is not None:
                        del comments[comment_idx]
                    if columns is not None:
                        table=table[0],columns
                    comment_lines=comment_lines+comments
                    if prev_key is not None:
                        data[prev_key]=InlineTable(table)
                    else:
                        raise IOError("inline table isn't attributed to any dict node")
                else:
                    comment_lines.append(line.lstrip("# \t"))
        line=f.readline()
    return (data,comment_lines)