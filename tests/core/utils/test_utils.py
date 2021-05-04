import pytest

import numpy as np



##### Basic import tests #####

def test_imports():
    """Test general non-failing of imports"""
    import pylablib.core.utils.array_utils
    import pylablib.core.utils.ctypes_wrap
    import pylablib.core.utils.dictionary
    import pylablib.core.utils.files
    import pylablib.core.utils.funcargparse
    import pylablib.core.utils.functions
    import pylablib.core.utils.general
    import pylablib.core.utils.indexing
    import pylablib.core.utils.ipc
    import pylablib.core.utils.library_parameters
    import pylablib.core.utils.module
    import pylablib.core.utils.net
    import pylablib.core.utils.numerical
    import pylablib.core.utils.observer_pool
    import pylablib.core.utils.py3
    import pylablib.core.utils.rpyc_utils
    import pylablib.core.utils.strdump
    import pylablib.core.utils.string
    import pylablib.core.utils.strpack
    import pylablib.core.utils.units




##### String tests #####

from pylablib.core.utils import string

def test_string():
    """Test to/from string conversion consistency"""
    # scalars
    for v in [True,False,None,0,1,2,1.5,1+2j,"abc","\n",r"\n",["\n"],[r"\n"]]:
        assert string.from_string(string.to_string(v))==v
    # lists/arrays
    assert string.to_string([1,2,3])=="[1, 2, 3]"
    assert string.from_string("[1, 2, '3']")==[1,2,"3"]
    assert string.to_string(np.arange(3))=="[0, 1, 2]"
    assert string.to_string(np.arange(3),use_classes=True)=="array([0, 1, 2])"
    assert string.from_string("[1,2,3+4j,(3+4j),[5,6,(7,8)],{'a':9,'b':10}]")==[1,2,3+4j,(3+4j,),[5,6,(7,8)],{'a':9,'b':10}]
    assert string.from_string("[1,2,(3+4j),(3+4j,),[5,6,(7,8)],{'a':9,'b':10}]",parenthesis_rules="python")==[1,2,3+4j,(3+4j,),[5,6,(7,8)],{'a':9,'b':10}]
    varlst=[1, 2, 3, 123, "\n", " ", "\t", r"\n", r"\t", "123", "abc",
        "[ 3, 4, '5']", "[6, 7, \"8\"]", (), "()", "(,)", (1,2, [3,4]), {"x":5, "y":10, "z":[15, (20,30)]}, {"a", b"b", r"\n\m"}, 
        None, True, False, 3.5, 1+2j, "", "1+2j", "(1+2j)", ("1+2j",), (1,), (1j,), (1+2j,), (("1+2j",),)]
    for pr in ["text","python"]:
        assert string.from_string(string.to_string(varlst,parenthesis_rules=pr),parenthesis_rules=pr)==varlst
        for loc in ["element","parameter","entry"]:
            for v in varlst:
                assert string.from_string(string.to_string(v,location=loc,parenthesis_rules=pr),parenthesis_rules=pr)==v
    nplst=[np.arange(3), [0,1,2]]
    assert string.from_string(string.to_string(nplst,use_classes=False))==[nplst[1],nplst[1]]
    assert isinstance(string.from_string(string.to_string(nplst,use_classes=True))[0],np.ndarray)
    assert np.all(string.from_string(string.to_string(nplst,use_classes=True))[0]==nplst[0])
    # tuples
    assert string.to_string((1,2,3))=="(1, 2, 3)"
    assert string.from_string("(1, 2, '3')")==(1,2,"3")
    assert string.from_string("(1,2,3+4j,(3+4j),[5,6,(7,8)],{'a':9,'b':10})")==(1,2,3+4j,(3+4j,),[5,6,(7,8)],{'a':9,'b':10})
    assert string.from_string("(1,2,(3+4j),(3+4j,),[5,6,(7,8)],{'a':9,'b':10})",parenthesis_rules="python")==(1,2,3+4j,(3+4j,),[5,6,(7,8)],{'a':9,'b':10})
    for pr in ["text","python"]:
        assert string.from_string(string.to_string(tuple(varlst),parenthesis_rules=pr),parenthesis_rules=pr)==tuple(varlst)


##### Dictionary tests #####

from pylablib.core.utils import dictionary

def test_dict():
    """Test dictionaries"""
    d=dictionary.Dictionary({"a":1,"b":2,"c/d":3,"c/e":4,"c/0":{"g":5,"f":6}})
    # path formats
    assert d["c/e"]==d["c","e"]
    assert d["c/e"]==d["c"][""]["e"]
    assert d["c/e"]==d["/c///e//"]
    assert d["c/e"]==d["c"]["/e//"]
    assert d["c/0/f"]==d["c"][0]["f"]
    assert d["c/0/f"]==d["c",0,"f"]
    # deleting
    assert "0/f" in d["c"]
    del d["c/0/f"]
    assert "0/f" not in d["c"]
    # replacing
    with pytest.raises(KeyError):
        d["c/0/g/x"]=10
    d.add_entry("c/0/g/x",10,force=True)
    # checking containment
    assert d["c/0/g/x"]==10
    assert d.has_entry("c/0/g/x")
    assert d.has_entry("c/0/g/x","leaf")
    assert not d.has_entry("c/0/g/x","branch")
    assert d.has_entry("c/0/g")
    assert not d.has_entry("c/0/g","leaf")
    assert d.has_entry("c/0/g","branch")
    # mapping / filtering
    d.map_self(lambda v: v*2)
    assert d["c/0/g/x"]==20
    d.filter_self(lambda v: v%4)
    assert "c/0/g/x" not in d
    assert "c/d" in d
    # replacing root
    d[""]={"a":1}
    assert d.asdict()=={"a":1}