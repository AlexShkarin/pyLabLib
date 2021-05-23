"""
Utilities for matplotlib plotting.
"""

from builtins import range

import matplotlib.pyplot as mpl
from . import dictionary, funcargparse
from ..dataproc import waveforms

import numpy as np

class IRecurrentPlot(object):
    """
    Recurrent plot.
    
    Can be used to plot multiple similar datasets in the same plot.
    
    First ploting call creates figure and axes (calling :meth:`plot_prepare` method);
    all consecutive calls only change the data (calling :meth:`plot_next` method).
    This way the figure is preserved between the plotting calls, which decreases resource consumption and minimizes matplotlib memory leaks.
    
    Args:
        fig (matplotlib.figure.Figure): If not ``None``, the figure to use for plotting.
        auto_clear (bool): If ``True``, clear plot (empty data) before each subsequent plotting.
        auto_relim (bool): If ``True``, rescale plot after each plotting.
        auto_layout (bool): If ``True``, call `tight_layout` after each plotting.
    """
    def __init__(self, fig=None, auto_clear=True, auto_relim=True, auto_layout=True):
        object.__init__(self)
        self.fig=fig
        self.prepared=False
        self.auto_relim=auto_relim
        self.auto_clear=auto_clear
        self.auto_layout=auto_layout
        self.lines=dictionary.Dictionary()
        
    def __setitem__(self, name, line):
        if isinstance(line,list) and len(line)==1:
            line=line[0]
        self.lines[name]=line
    def __getitem__(self, name):
        return self.lines[name]
    
    def plot_prepare(self, *args, **vargs):
        """
        Prepare plot.
        
        Abstract method, has to be overloaded in subclasses.
        
        Called once before the first plotting happens.
        """
        raise NotImplementedError("IRecurrentPlot.plot_prepare")
    def plot_clear(self):
        """Clear the ploted data."""
        for p in self.lines.iternodes():
            try:
                p.set_data([],[])
            except AttributeError:
                pass
        return self
    def plot_next(self, *args, **kwargs):
        """
        Plot data.
        
        Abstract method, has to be overloaded in subclasses.
        
        Called every time the data is updated.
        """
        raise NotImplementedError("IRecurrentPlot.plot_next")
    
    def setup_figure(self):
        """
        Create a figure if it hasn't been created already.
        """
        if self.fig is None:
            self.fig=mpl.figure()
    def setup_prepare(self, *args, **kwargs):
        """
        Prepare the plot if it hasn't been prepared already.
        """
        if not self.prepared:
            self.setup_figure()
            self.plot_prepare(*args,**kwargs)
            self.prepared=True
    def plot(self, *args, **kwargs):
        """
        Plot the data.
        
        The supplied arguments are redirected to the overloaded methods :meth:`plot_prepare` and :meth:`plot_next`.
        """
        self.setup_prepare(*args,**kwargs)
        if self.auto_clear:
            self.plot_clear()
        self.plot_next(*args,**kwargs)
        if self.auto_relim:
            for plt in self.fig.axes:
                plt.relim()
                plt.autoscale_view()
        if self.auto_layout:
            self.fig.tight_layout()
        return self
    def savefig(self, path, *args, **kwargs):
        """
        Save the figure to the location defined by `path`.
        
        Arguments are passed to :meth:`matplotlib.figure.Figure.savefig`.
        """
        if self.fig is not None:
            self.fig.savefig(path,*args,**kwargs)
        return self
    def close(self):
        """Clear and close the figure."""
        if self.fig is not None:
            for plt in self.fig.axes:
                plt.cla()
            self.fig.clf()
            mpl.close(self.fig)
            self.fig=None
            self.prepared=False
            
            
            
            
class GenericPlotter(IRecurrentPlot):
    """
    Generic multi-axes plotter.
    
    Args:
        axes_num (int): Number of axes in the figure (all are aligned vertically).
        plots_num: Number of plot lines;
            can be either an integer (all plots have the same number of lines) or an integer list of length `axes_num`.
        axes_names ([str]): Names of axes for referencing in plotting (ordered integers by default).
        log_x/log_y: Use log scale for x/y axes;
            can be either a single bool (all plots have the same scale) or list of a bool list of length `axes_num`.
        xlabel/ylabel: Labels for for x/y axes;
            can be either a single string (all plots have the same axes labels) or a string list with length `axes_num`.
        legend ([str]): Plot legends
        xscale/yscale: Scales for x/y axes (supplied data is multiplied by these scales before plotting);
            can be either a single float (all axes have the same scale)
            or list of floats with length `axes_num` (all plots in the same axes have the same scale)
            or list of lists of floats (specifies scale for each line in each plot separately)
        fig (matplotlib.figure.Figure): If not ``None``, the figure to use for plotting.
    """
    def __init__(self, axes_num=1, plots_num=1, axes_names=None, log_x=False, log_y=False, xlabel="", ylabel="", legend=None, xscale=1., yscale=1., fig=None):
        IRecurrentPlot.__init__(self,fig=fig)
        self.axes_num=axes_num
        self.axes_names=axes_names or list(range(axes_num))
        self.plots_num=funcargparse.as_sequence(plots_num,axes_num)
        #plot_names=funcargparse.as_sequence(plot_names,axes_num)
        #self.plot_names=[funcargparse.as_sequence(pns,pn) if pn else range(pn) for pn,xs in zip(self.plots_num,plot_names)]
        self.plot_names=[list(range(pn)) for pn in self.plots_num]
        self.log_x=funcargparse.as_sequence(log_x,axes_num)
        self.log_y=funcargparse.as_sequence(log_y,axes_num)
        self.xlabel=funcargparse.as_sequence(xlabel,axes_num)
        self.ylabel=funcargparse.as_sequence(ylabel,axes_num)
        xscale=funcargparse.as_sequence(xscale,axes_num)
        yscale=funcargparse.as_sequence(yscale,axes_num)
        self.xscale=[funcargparse.as_sequence(xs,pn) for pn,xs in zip(self.plots_num,xscale)]
        self.yscale=[funcargparse.as_sequence(ys,pn) for pn,ys in zip(self.plots_num,yscale)]
        #legend=funcargparse.as_sequence(legend,axes_num)
        #self.legend=[funcargparse.as_sequence(l,pn,allowed_type="builtin;nostring") for pn,l in zip(self.plots_num,legend)]
        self.legend=funcargparse.as_sequence(legend,axes_num)
    def plot_prepare(self, *args, **kwargs):
        """
        Prepare the plot if it hasn't been prepared already.
        """
        for a in range(self.axes_num):
            an=self.axes_names[a]
            ax=self.fig.add_subplot(self.axes_num,1,a+1)
            for pn in self.plot_names[a]:
                self[an,pn]=ax.plot([],[])
            if self.log_x[a]:
                ax.set_xscale("log")
            if self.log_y[a]:
                ax.set_yscale("log")
            ax.set_xlabel(self.xlabel[a])
            ax.set_ylabel(self.ylabel[a])
            ax.grid(which="both")
    def plot_next(self, data, legend=None):
        """
        Plot data.
        
        Data is a list of lists ``[axes_num][plot_num]`` of 1D or 2D 2-columns array.
        """
        data=funcargparse.as_sequence(data,self.axes_num,allowed_type="builtin;nostring")
        legend=funcargparse.as_sequence(legend,self.axes_num,allowed_type="builtin;nostring") if (legend is not None) else self.legend
        for a in range(self.axes_num):
            an=self.axes_names[a]
            ad=funcargparse.as_sequence(data[a],self.plots_num[a],allowed_type="builtin;nostring")
            l=legend[a]
            for p,pn in enumerate(self.plot_names[a]):
                d=np.asarray(ad[p])
                xs,ys=self.xscale[a][p],self.yscale[a][p]
                if np.ndim(d)==1:
                    self[an,pn].set_data(np.arange(len(d))*xs,d*ys)
                else:
                    self[an,pn].set_data(d[:,0]*xs,d[:,1]*ys)
            if l is not None:
                self.fig.axes[a].legend(l)
            else:
                self.fig.axes[a].legend([]).set_visible(False)
                
                
            
def add_all_subplots(fig, r, c=None, *args, **vargs):
    if c is None:
        r,c=r//10,r%10
    for n in range(1,r*c+1):
        fig.add_subplot(r,c,n,*args,**vargs)
    return fig.axes[-r*c:]



def iterlabels(obj, include=["axes","ticks","title"]):
    """
    Iterate over text labels in `obj`.
    
    Args:
        obj: can be a single ``Axes`` or a ``Figure`` (in which case iteration goes over all contained axes).
        include ([str]): determines which kind of labels are iterated over. Can contain ``"axes"`` (axes label), ``"ticks"`` (axes tick labels) and ``"title"`` (plot title).
    """
    if isinstance(obj,mpl.Figure):
        for ax in obj.axes:
            for lab in iterlabels(ax, include=include):
                yield lab
        return
    if "axes" in include:
        yield obj.xaxis.label
        yield obj.yaxis.label
    if "ticks" in include:
        for lab in obj.get_xticklabels()+obj.get_yticklabels():
            yield lab
    if "title" in include:
        yield obj.title



def plot_func(func, rng, *args, **kwargs):
    """
    Plot a callable function over a given range.

    `rng` is a tuple `(start, stop, points_number)` passed to :func:`numpy.linspace` to generate plot points.
    The rest of the arguments is the same as in :func:`matplotlib.pyplot.plot`.
    """
    xs=np.linspace(*rng)
    mpl.plot(xs,func(xs),*args,**kwargs)

def plot_columns(data, x_column, y_column, *args, **kwargs):
    """
    Plot two data columns vs each other.
    """
    xs=waveforms.get_x_column(data,x_column)
    ys=waveforms.get_y_column(data,y_column)
    mpl.plot(xs,ys,*args,**kwargs)