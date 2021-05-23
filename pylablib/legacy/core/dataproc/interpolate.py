from builtins import range

import numpy as np
import scipy.interpolate

from . import waveforms
from ..datatable import wrapping


def _data_range(data):
    return (np.min(data),np.max(data))

def interpolate1D_func(x, y, kind="linear", axis=-1, copy=True, bounds_error=True, fill_values=np.nan, assume_sorted=False):
    """
    1D interpolation.
    
    Simply a wrapper around :class:`scipy.interpolate.interp1d`.

    Args:
        x: 1D arrays of x coordinates for the points at which to find the values.
        y: array of values corresponding to x points (can have more than 1 dimension, in which case the output values are (N-1)-dimensional)
        kind: Interpolation method.
        axis: axis in y-data over which to interpolate.
        copy: if ``True``, make internal copies of `x` and `y`.
        bounds_error: if ``True``, raise error if interpolation function arguments are outside of `x` bounds.
        fill_values: values to fill the outside-bounds regions if ``bounds_error==False``.
        assume_sorted: if ``True``, assume that `data` is sorted.
    Returns:
        A 1D array with interpolated data.
    """
    if fill_values=="bounds":
        fill_values=tuple(np.take(y,[x.argmin(),x.argmax()],axis=axis))
        bounds_error=False
    return scipy.interpolate.interp1d(x,y,kind=kind,axis=axis,copy=copy,bounds_error=bounds_error,fill_value=fill_values,assume_sorted=assume_sorted)


def interpolate1D(data, x, kind="linear", bounds_error=True, fill_values=np.nan, assume_sorted=False):
    """
    1D interpolation.
    
    Args:
        data: 2-column array [(x,y)], where ``y`` is a function of ``x``.
        x: Arrays of x coordinates for the points at which to find the values.
        kind: Interpolation method.
        bounds_error: if ``True``, raise error if `x` values are outside of `data` bounds.
        fill_values: values to fill the outside-bounds regions if ``bounds_error==False``
        assume_sorted: if ``True``, assume that `data` is sorted.
    Returns:
        A 1D array with interpolated data.
    """
    return interpolate1D_func(data[:,0],data[:,1],kind=kind,bounds_error=bounds_error,fill_values=fill_values,assume_sorted=assume_sorted)(x)

def interpolate2D(data, x, y, method="linear", fill_value=np.nan):
    """
    Interpolate data in 2D.
    
    Simply a wrapper around :func:`scipy.interpolate.griddata`.
    
    Args:
        data: 3-column array [(x,y,z)], where ``z`` is a function of ``x`` and ``y``.
        x/y: Arrays of x and y coordinates for the points at which to find the values.
        method: Interpolation method.
    Returns:
        A 2D array with interpolated data.
    """
    interp_data=scipy.interpolate.griddata((data[:,0],data[:,1]),data[:,2],(x,y),method=method,fill_value=fill_value)
    return interp_data

def interpolateND(data, xs, method="linear"):
    """
    Interpolate data in N dimensions.
    
    Simply a wrapper around :func:`scipy.interpolate.griddata`.
    
    Args:
        data: ``(N+1)``-column array ``[(x_1,..,x_N,y)]``, where ``y`` is a function of ``x_1, ... ,x_N``.
        xs: ``N``-tuple of arrays of coordinates for the points at which to find the values.
        method: Interpolation method.
    Returns:
        An ND array with interpolated data.
    """
    coords=tuple([data[:,n] for n in range(data.shape[1]-1)])
    interp_data=scipy.interpolate.griddata(coords,data[:,-1],xs,method=method)
    return interp_data
        



def regular_grid_from_scatter(data, x_points, y_points, x_range=None, y_range=None, method="nearest"):
    """
    Turn irregular scatter-points data into a regular 2D grid function.
    
    Args:
        data: 3-column array ``[(x,y,z)]``, where ``z`` is a function of ``x`` and ``y``.
        x_points/y_points: Number of points along x/y axes.
        x_range/y_range: If not ``None``, a tuple specifying the desired range of the data (all points in `data` outside the range are excluded).
        method: Interpolation method (see :func:`scipy.interpolate.griddata` for options).
    Returns:
        A nested tuple ``(data, (x_grid, y_grid))``, where all entries are 2D arrays (either with data or with gridpoint locations).
    """
    if x_range is not None:
        data=waveforms.cut_to_range(data,x_range,0)
    else:
        x_range=_data_range(data[:,0])
    if y_range is not None:
        data=waveforms.cut_to_range(data,y_range,1)
    else:
        y_range=_data_range(data[:,1])
    x_grid=np.linspace(x_range[0],x_range[1],x_points)
    y_grid=np.linspace(y_range[0],y_range[1],y_points)
    xi,yi=np.meshgrid(x_grid,y_grid)
    interp_data=scipy.interpolate.griddata((data[:,0],data[:,1]),data[:,2],(xi,yi),method=method)
    return interp_data,(x_grid,y_grid)


def interpolate_trace(trace, step, rng=None, x_column=0, select_columns=None, kind="linear", assume_sorted=False,):
    """
    Interpolate trace data over a regular grid with the given step.

    `rng` specifies interpolation range (by default, whole data range).
    `x_column` specifies column index for x-data.
    `select_column` specifies which columns to interpolate and keep at the output (by default, all data).
    If ``assume_sorted==True``, assume that x-data is sorted.
    `kind` specifies interpolation method.
    """
    wtrace=wrapping.wrap(trace)
    src_column=waveforms.get_x_column(trace,x_column=x_column)
    select_columns=select_columns or range(wtrace.shape()[1])
    rng_min,rng_max=rng or (None,None)
    rng_min=src_column.min() if (rng_min is None) else rng_min
    rng_max=src_column.max() if (rng_max is None) else rng_max
    start=(rng_min//step)*step
    stop=(rng_max//step)*step
    pts=np.arange(start,stop+step/2.,step)
    xidx=wtrace.c.get_index(x_column)
    columns=[ pts if wtrace.c.get_index(c)==xidx else
            interpolate1D_func(src_column,wtrace[:,c],kind=kind,bounds_error=False,fill_values="bounds",assume_sorted=assume_sorted)(pts)
            for c in select_columns]
    return wtrace.subtable((slice(None),select_columns)).columns_replaced(columns,wrapped=False)


def average_interpolate_1D(data, step, rng=None, avg_kernel=1, min_weight=0, kind="linear"):
    """
    1D interpolation combined with pre-averaging.
    
    Args:
        data: 2-column array [(x,y)], where ``y`` is a function of ``x``.
        step: distance between the points in the interpolated data (all resulting x-coordinates are multiples of `step`).
        rng: if not ``None``, specifies interpolation range (by default, whole data range).
        avg_kernel: kernel used for initial averaging. Can be either a 1D array, where each point corresponds to the relative bin weight,
            or an integer, which specifies simple rectangular kernel of the given width.
        min_weight: minimal accumulated weight in the bin to consider it 'valid'
            (if the bin is invalid, its accumulated value is ignored, and its value is obtained by the interpolation step).
            `min_weight` of 0 implies any non-zero weight; otherwise, weight ``>=min_weight``.
        kind: Interpolation method.
    Returns:
        A 2-column array with the interpolated data.
    """
    if isinstance(avg_kernel,(int,float)):
        avg_kernel=max(int(avg_kernel)//2,0)*2+1
        avg_kernel=np.ones(avg_kernel)
    rng_min,rng_max=rng or (None,None)
    rng_min=data[:,0].min() if (rng_min is None) else rng_min
    rng_max=data[:,0].max() if (rng_max is None) else rng_max
    rng=(rng_min,rng_max)
    rng=[(l//step)*step for l in rng]
    bins=np.linspace(rng[0],rng[1],int((rng[1]-rng[0])/step)+1)
    locs=bins.searchsorted(data[:,0])
    locs[locs==len(bins)]-=1
    bindiffs=data[:,0]-bins[locs]
    locs[(locs>0)&(bindiffs<-step/2.)]-=1
    sums=np.zeros((len(bins)))
    np.add.at(sums,locs,data[:,1])
    weights=np.zeros((len(bins)))
    np.add.at(weights,locs,1)
    sums=np.convolve(sums,avg_kernel,mode="same")
    weights=np.convolve(weights,avg_kernel,mode="same")
    filled=weights>min_weight if min_weight==0 else weights>=min_weight
    intx=bins[filled]
    inty=sums[filled]/weights[filled]
    data=interpolate1D_func(intx,inty,kind=kind,bounds_error=False,fill_values="bounds",assume_sorted=True)(bins)
    return np.column_stack((bins,data))