import pytest

import pandas as pd
import numpy as np
import os

from .cmp_utils import compare_tables, compare_column, compare_row

@pytest.fixture(params=["array","pandas"])
def table_builder(request):
    """Function which returns a table of a given kind (numpy array or pandas table) from data and column names"""
    kind=request.param
    def _builder(data, columns, index=None):
        if kind=="array":
            res=np.array(data)
        else:
            res=pd.DataFrame(data,columns=columns,index=index)
        _checker(res,columns)
        return res
    def _checker(data, columns, index=None, l=None):
        if kind=="array":
            assert isinstance(data,np.ndarray)
        else:
            assert isinstance(data,pd.DataFrame)
            assert list(data.columns)==columns
            if index is not None:
                assert np.all(data.index==index)
        assert data.ndim==2
        assert data.shape[1]==len(columns)
        if l is not None:
            assert data.shape[0]==l
    _builder.kind=kind
    _builder.check=_checker
    _builder.tcmp=compare_tables
    _builder.rcmp=compare_column
    _builder.ccmp=compare_row
    return _builder


from pylablib.core.fileio import loadfile

@pytest.fixture
def table_loader(table_builder, root_path):
    """Function which loads a table of a given kind (numpy array or pandas table) from the text file given the column names"""
    def _loader(path, columns, index=None):
        data=loadfile.load_csv(os.path.join(root_path,path),out_type="array")
        return table_builder(data,columns,index=index)
    _loader.kind=table_builder.kind
    _loader.builder=table_builder
    return _loader