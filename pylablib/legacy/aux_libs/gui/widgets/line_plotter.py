"""
Simple PyQtGraph-based line plotter.

A small expansion on top of :class:`.pyqtgraph.PlotWidget` which allows for thread-safe plot updating.
"""

import pyqtgraph


class LinePlotter(pyqtgraph.PlotWidget):
    """
    Line plotter object.

    Built on top of :class:`.pyqtgraph.PlotWidget` class.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None):
        super(LinePlotter, self).__init__(parent)
        self.data={}
        self._traces={}
        self.trace_names=[]
        self.updated=True
        self.addLegend()
        self.setLabel("left","Signal")
        self.showGrid(True,True,0.7)

    def add_trace(self, name, caption=None, *args, **kwargs):
        """
        Add a trace plot.

        If caption is not ``None``, the trace is also added into the legend under the given caption.
        All other arguments are passed to the underlying :meth:`.pyqtgraph.PlotWidget.plot` method.
        """
        if name in self._traces:
            raise ValueError("trace {} already exists".format(name))
        if caption is not None:
            kwargs["name"]=caption
        line=self.plot([],[],*args,**kwargs)
        self._traces[name]=(line,caption)
        self.trace_names.append(name)
    def delete_trace(self, name):
        """Delete trace plot"""
        line,caption=self._traces.pop(name)
        self.trace_names.remove(name)
        self.removeItem(line)
        if caption is not None:
            self.plotItem.legend.removeItem(caption)

    def set_traces(self, data, hide_missing=True):
        """
        Set data to be plotted.

        `data` is a list or a dictionary of 2-column numpy arrays containing x- and y-coordinates of the plots.
        If it is a list, the columns are assumed to be in the order of their creation (also available as ``trace_names`` attribute).
        If it is a dictionary, the keys are the column names.
        If ``hide_missing==True`` and some traces are missing from the data, hide them (although they still appear in the legend);
        otherwise, the missing traces are left unchanged.

        This function is thread-safe (i.e., the application state remains consistent if it's called from another thread,
        although race conditions on simultaneous calls from multiple threads still might happen).
        """
        if isinstance(data,list):
            self.data=dict(zip(self.trace_names,data))
        else:
            self.data=data.copy()
        if hide_missing:
            for n in self.trace_names:
                if n not in self.data:
                    self.data[n]=[]
        self.updated=True

    def update_traces(self, only_new_data=True):
        """
        Update displayed traces.

        If ``only_new_data==True`` and the data hasn't changed since the last call to ``update_traces``, skip replotting.
        """
        if (not only_new_data) or self.updated:
            self.updated=False
            for n in self.trace_names:
                if n in self.data:
                    t=self.data[n]
                    if len(t):
                        self._traces[n][0].setData(t[:,0],t[:,1])
                    else:
                        self._traces[n][0].setData([],[])