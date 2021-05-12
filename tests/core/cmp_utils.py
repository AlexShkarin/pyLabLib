import pandas as pd
import numpy as np

from pylablib.core.utils.dictionary import as_dict

def _cmp(v1, v2, decimal):
    if decimal is None:
        np.testing.assert_array_equal(v1,v2)
    else:
        np.testing.assert_array_almost_equal(v1,v2,decimal=decimal)
def compare_tables(t1, t2, decimal=None):
    """Compare two tables (type, shape, content, etc.)"""
    assert type(t1)==type(t2)
    assert isinstance(t1,(np.ndarray,pd.DataFrame))
    assert np.shape(t1)==np.shape(t2)
    _cmp(t1,t2,decimal)
    if isinstance(t1,pd.DataFrame):
        assert np.all(t1.columns==t2.columns)
        assert np.all(t1.index==t2.index)

def compare_column(t, index, c, decimal=None):
    """Compare a given column in the table with the expected result"""
    assert isinstance(t,(np.ndarray,pd.DataFrame))
    if isinstance(t,np.ndarray):
        tc=t[:,index]
    else:
        tc=t[index]
    _cmp(tc,c,decimal)
def compare_row(t, index, r, decimal=None):
    """Compare a given row in the table with the expected result"""
    assert isinstance(t,(np.ndarray,pd.DataFrame))
    if isinstance(t,np.ndarray):
        tr=t[index,:]
    else:
        tr=t.iloc[index]
    _cmp(tr,r,decimal)

def compare_dicts(d1, d2, decimal=None):
    assert type(d1)==type(d2)
    d1=as_dict(d1,"flat").copy()
    d2=as_dict(d2,"flat").copy()
    for k in list(d1):
        if isinstance(d1[k],(pd.DataFrame,np.ndarray)):
            compare_tables(d1[k],d2[k],decimal=decimal)
            del d1[k]
            del d2[k]
    assert d1==d2