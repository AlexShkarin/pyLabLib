import numpy as np
import pandas as pd

from ..cmp_utils import compare_tables


##### Basic import tests #####

def test_imports():
    """Test general non-failing of imports"""
    import pylablib.core.dataproc.callable
    import pylablib.core.dataproc.feature
    import pylablib.core.dataproc.filters
    import pylablib.core.dataproc.fitting
    import pylablib.core.dataproc.fourier
    import pylablib.core.dataproc.iir_transform
    import pylablib.core.dataproc.image
    import pylablib.core.dataproc.interpolate
    import pylablib.core.dataproc.specfunc
    import pylablib.core.dataproc.table_wrap
    import pylablib.core.dataproc.utils


from pylablib.core.dataproc import filters, fourier, utils

def test_utils(table_loader):
    builder=table_loader.builder
    cols=["col1","col2"]
    data=table_loader("core/dataproc/data_raw.csv",columns=cols)
    if builder.kind=="pandas":
        index=data.index=data.index**2
    else:
        index=None
    cindex=np.array(index) if index is not None else np.arange(len(data))
    adata=np.array(data)
    def asarr(data, check_index=True):
        builder.check(data,cols,index=index if check_index else None)
        return np.array(data)
    # properties
    for t,a,d,l in [(np.arange(100),True,False,True),(-np.arange(100),False,True,True),(np.arange(100)**2,True,False,False),(adata[:100,0],False,False,False)]:
        wt=builder(t[:,None],["column"])
        assert utils.is_ascending(wt)==a
        assert utils.is_descending(wt)==d
        assert utils.is_ordered(wt)==a or d
        assert utils.is_linear(wt)==l
    # columns
    np.testing.assert_array_almost_equal(utils.get_x_column(data),adata[:,0])
    np.testing.assert_array_almost_equal(utils.get_x_column(data,0),adata[:,0])
    np.testing.assert_array_almost_equal(utils.get_x_column(data,1),adata[:,1])
    np.testing.assert_array_almost_equal(utils.get_x_column(data,"#"),cindex)
    np.testing.assert_array_almost_equal(utils.get_y_column(data),adata[:,1])
    np.testing.assert_array_almost_equal(utils.get_y_column(data,0),adata[:,0])
    np.testing.assert_array_almost_equal(utils.get_y_column(data,1),adata[:,1])
    np.testing.assert_array_almost_equal(utils.get_y_column(data,"#"),cindex)
    # sorting
    for c in [0,1]:
        sdata=utils.sort_by(data,c)
        asdata=asarr(sdata,check_index=False)
        assert utils.is_ascending(asdata[:,c])
    if builder.kind=="pandas":
        sdata=utils.sort_by(data,"col2")
        asdata=asarr(sdata,check_index=False)
        assert utils.is_ascending(asdata[:,1])
    # cutting / closest
    adata=np.column_stack([np.arange(100)**2,np.random.normal(size=100)])
    data=builder(adata,cols)
    assert utils.find_closest_arg(adata[:,0],101)==10
    assert utils.find_closest_value(adata[:,0],101)==100
    for flipped in [True,False]:
        d=data[::-1] if flipped else data
        ads=-1 if flipped else 1
        for ordered in [True,False]:
            for rng,irng in [((None,101),(0,11)),((99,2501),(10,51))]:
                cdata=utils.cut_to_range(d,rng,ordered=ordered)
                acdata=asarr(cdata,check_index=False)
                np.testing.assert_array_almost_equal(acdata,adata[irng[0]:irng[1]][::ads])
    # wrapping / disc_step
    assert abs(utils.find_discrete_step(np.random.randint(100,size=100)*np.pi)-np.pi)<1E-6
    np.testing.assert_array_almost_equal(utils.unwrap_mod_data(np.arange(100)**.5%3,3),np.arange(100)**.5)


def test_filters(table_loader):
    builder=table_loader.builder
    cols=["col1","col2"]
    data=table_loader("core/dataproc/data_raw.csv",columns=cols)
    if builder.kind=="pandas":
        index=data.index=data.index**2
    else:
        index=None
    adata=np.array(data)
    l0=len(adata)
    def asarr(data, check_index=True, l=None):
        builder.check(data,cols,index=index if check_index else None,l=l or l0)
        return np.array(data)
    # Gaussian filter
    gfldata=table_loader("core/dataproc/data_gaussian_filter.csv",columns=cols,index=index)
    compare_tables(filters.gaussian_filter(data,5),gfldata,decimal=4)
    compare_tables(filters.gaussian_filter_nd(data,5),gfldata,decimal=6)
    # IIR/int/diff
    t=77
    lpdata=filters.low_pass_filter(data,t)
    alpdata=asarr(lpdata)
    compare_tables((alpdata[1:]-alpdata[:-1]*np.exp(-1/t))/(1-np.exp(-1/t)),adata[1:],decimal=6)
    hpdata=filters.high_pass_filter(data,t)
    ahpdata=asarr(hpdata)
    compare_tables(adata-alpdata,ahpdata,decimal=6)
    idata=filters.integrate(data)
    aidata=asarr(idata)
    compare_tables(np.cumsum(adata,axis=0),aidata,decimal=6)
    ddata=filters.differentiate(data)
    addata=asarr(ddata,check_index=False,l=l0-1)
    compare_tables(adata[1:]-adata[:-1],addata,decimal=6)
    # sliding
    sadata=filters.sliding_average(data,5)
    asadata=asarr(sadata)
    assert np.all(asadata[10]==np.mean(adata[8:13],axis=0))
    smdata=filters.median_filter(data,5)
    asmdata=asarr(smdata)
    assert np.all(asmdata[10]==np.median(adata[8:13],axis=0))
    dec_funcs={"mean":np.mean,"max":np.max,"min":np.min,"sum":np.sum,"median":np.median,"skip":None}
    for n,f in dec_funcs.items():
        if n!="skip":
            sfdata=filters.sliding_filter(data,5,dec=n)
            asfdata=asarr(sfdata)
            assert np.all(asfdata[10]==f(adata[8:13],axis=0))
    # decimation
    for n,f in dec_funcs.items():
        if n!="skip":
            dfdata=filters.decimate(data,5,dec=n)
            adfdata=asarr(dfdata,check_index=False,l=l0//5)
            assert np.all(adfdata[10]==f(adata[50:55],axis=0))
            dddata=filters.decimate_datasets([data,data*10,data+10],dec=n)
            adddata=asarr(dddata)
            assert np.all(adddata==f([adata,adata*10,adata+10],axis=0))
            assert np.all(filters.decimate_full(data,dec=n)==f(adata,axis=0))
    compare_tables(filters.binning_average(data,5),filters.decimate(data,5,"bin"))
    # Fourier
    ffldata=table_loader("core/dataproc/data_fourier_filter.csv",columns=cols,index=index)
    resp=filters.fourier_filter_bandpass(0.1-1E-5,0.2-1E-5)
    compare_tables(filters.fourier_filter(data,resp),ffldata,decimal=6)
    resp=filters.fourier_filter_bandstop(0.1-1E-5,0.2-1E-5)
    compare_tables(filters.fourier_filter(data,resp),data-ffldata,decimal=6)
    # Running
    for dec in ["mean","min"]:
        flt=filters.RunningDecimationFilter(10,mode=dec)
        pfdata=filters.sliding_filter(adata[:,0],10,dec=dec)[5:-5]
        rfdata=np.array([flt.add(x) for x in adata[:,0]][10:])
        compare_tables(rfdata,pfdata,decimal=6)
        flt.reset()
        rfdata=np.array([flt.add(x) for x in adata[:,0]][10:])
        compare_tables(rfdata,pfdata,decimal=6)

def test_fourier(table_loader):
    builder=table_loader.builder
    cols=["col1","col2"]
    data=table_loader("core/dataproc/data_raw.csv",columns=cols)
    data=data[data.columns[:1]] if builder.kind=="pandas" else data[:,:1]
    adata=np.array(data)[:,0]
    def asarr(data, columns=None):
        builder.check(data,columns=columns,l=len(adata))
        return np.array(data)
    dt=1E-3
    df=1/(dt*len(adata))
    # direct transform
    eftdata=np.fft.fftshift(np.fft.fft(adata))
    ftdata=fourier.fourier_transform(data,dt=1E-3)
    aftdata=asarr(ftdata,columns=["frequency","ft_data"])
    compare_tables(aftdata[:,1],eftdata,decimal=6)
    compare_tables(fourier.fourier_transform(data,dt=1E-3,raw=True),eftdata,decimal=6)
    # power spectral density
    psd=fourier.power_spectral_density(data,dt=1E-3,normalization="none")
    apsd=asarr(psd,columns=["frequency","PSD"])
    compare_tables(apsd[:,1],abs(eftdata)**2,decimal=6)
    assert np.all(abs(apsd[1:,0]-apsd[:-1,0]-df)<1E-6)
    psd=fourier.power_spectral_density(data,dt=1E-3,normalization="density")
    apsd=asarr(psd,columns=["frequency","PSD"])
    assert abs(np.sum(apsd[:,1])*df-np.mean(abs(adata)**2))<1E-6
    # inverse transform
    iftdata=fourier.inverse_fourier_transform(ftdata)
    aiftdata=asarr(iftdata,columns=["time","data"])
    compare_tables(aiftdata[:,1].real,adata,decimal=6)
    assert np.all(abs(aiftdata[1:,0]-aiftdata[:-1,0]-dt)<1E-6)