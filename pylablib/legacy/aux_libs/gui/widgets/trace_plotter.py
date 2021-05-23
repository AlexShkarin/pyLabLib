"""
PyQtGraph-based trace plotter.

Has 2 parts: :class:`TracePlotter` which displays the plots,
and :class:`TracePlotterController` which controls the channels (X-axis, enabled channels) and the plotting (buffer size, updating, etc.)
:class:`TracePlotter` can also operate alone without a controller.
When both are used, :class:`TracePlotter` is created and set up first, and then supplied to :meth:`TracePlotterController.setupUi` method.
"""

from .param_table import ParamTable
from ....core.gui.qt.thread import controller
from ....core.gui.qt import values as values_module
from ....core.utils import funcargparse, dictionary
from ....core.dataproc import waveforms
from ..helpers import TableAccumulator, TableAccumulatorThread

from PyQt5 import QtWidgets, QtCore
import pyqtgraph
import numpy as np


class TracePlotterController(QtWidgets.QWidget):
    """
    Class for controlling traces inside :class:`TracePlotter`.

    Like most widgets, requires calling :meth:`setupUi` to set up before usage.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None):
        super(TracePlotterController, self).__init__(parent)

    def setupUi(self, name, plotter, display_table=None, display_table_root=None):
        """
        Setup the trace plotter controller.

        Args:
            name (str): widget name
            plotter (TracePlotter): controlled image plotter
            display_table (bool): as :class:`.IndicatorValuesTable` object used to access table values; by default, create one internally
            display_table_root (str): if not ``None``, specify root (i.e., path prefix) for values inside the table.
        """
        self.display_table=display_table or values_module.IndicatorValuesTable()
        self.display_table_root=display_table_root or ""
        self.plotter=plotter
        self.plotter._attach_controller(self)

        self.name=name
        self.setObjectName(self.name)
        self.hLayout = QtWidgets.QVBoxLayout(self)
        self.hLayout.setContentsMargins(0,0,0,0)
        self.hLayout.setObjectName("hLayout")
        self.channelsGroupBox = QtWidgets.QGroupBox(self)
        self.channelsGroupBox.setObjectName("channelsGroupBox")
        self.channelsGroupBox.setTitle("Channels")
        self.channelsGroupLayout = QtWidgets.QVBoxLayout(self.channelsGroupBox)
        self.channelsGroupLayout.setContentsMargins(0, 0, 0, -1)
        self.channelsGroupLayout.setObjectName("channelsGroupLayout")
        self.channels_table = ParamTable(self.channelsGroupBox)
        self.channels_table.setMinimumSize(QtCore.QSize(20, 20))
        self.channels_table.setObjectName("channels_table")
        self.channelsGroupLayout.addWidget(self.channels_table)
        self.hLayout.addWidget(self.channelsGroupBox)
        self.plottingGroupBox = QtWidgets.QGroupBox(self)
        self.plottingGroupBox.setObjectName("plottingGroupBox")
        self.plottingGroupBox.setTitle("Plotting")
        self.plottingGroupLayout = QtWidgets.QHBoxLayout(self.plottingGroupBox)
        self.plottingGroupLayout.setContentsMargins(0, 0, 0, -1)
        self.plottingGroupLayout.setObjectName("plottingGroupLayout")
        self.plot_params_table = ParamTable(self.plottingGroupBox)
        self.plot_params_table.setMinimumSize(QtCore.QSize(20, 20))
        self.plot_params_table.setObjectName("plot_params_table")
        self.plottingGroupLayout.addWidget(self.plot_params_table)
        self.hLayout.addWidget(self.plottingGroupBox)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.hLayout.addItem(spacerItem)
        self.hLayout.setStretch(2, 1)

        self.channels_table.setupUi("channels",add_indicator=False,display_table=self.display_table,display_table_root=self.display_table_root+"/channels")
        self.setup_channels()
        self.plot_params_table.setupUi("plotting_params",add_indicator=False,display_table=self.display_table,display_table_root=self.display_table_root+"/plotting")
        self.plot_params_table.add_button("update_plot","Updating",checkable=True)
        self.plot_params_table.add_num_edit("disp_last",1,limiter=(1,None,"coerce","int"),formatter=("int"),label="Display last: ")
        self.plot_params_table.add_button("reset_history","Reset").value_changed_signal().connect(self.plotter.reset_history)

    def get_all_values(self):
        """Get all control values"""
        return self.display_table.get_all_values(root=self.display_table_root)
    def set_all_values(self, params):
        """Set all control values"""
        self.display_table.set_all_values(params,root=self.display_table_root)
    def get_all_indicators(self):
        """Get all GUI indicators as a dictionary"""
        return self.params_table.get_all_indicators(root=self.display_table_root)

    def setup_channels(self):
        """
        Update channels from the associated plotter.

        Sets up GUI appearance (dropdown menu items and checkbox rows) to correspond to the trace plotter settings.
        Called automatically on creation or channels update, doesn't need to be called explicitly.
        """
        self.channels_table.clear()
        if self.plotter.channel_indices:
            channel_names=[self.plotter.channels[idx]["name"] for idx in self.plotter.channel_indices]
            self.channels_table.add_combo_box("xaxis",0,options=channel_names,label="X axis")
            self.channels_table.add_combo_box("order_by",0,options=channel_names,label="Order by")
            for idx in self.plotter.channel_indices:
                name=self.plotter.channels[idx]["name"]
                self.channels_table.add_check_box(idx+"_enabled",name)
    def get_enabled_channels(self):
        """Get a list of enabled channels"""
        return [idx for idx in self.plotter.channel_indices if self.channels_table.v[idx+"_enabled"]]


class TracePlotter(QtWidgets.QWidget):
    """
    Trace plotter object.

    Built on top of :class:`.pyqtgraph.PlotWidget` class.

    Intended for plotting of gradually-accumulated data;
    designed to work tightly with :class:`.TableAccumulator` or :class:`.TableAccumulatorThread` as data sources.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None):
        super(TracePlotter, self).__init__(parent)

    def setupUi(self, name, add_end_marker=False, update_only_on_visible=True):
        """
        Setup the image view.

        Args:
            name (str): widget name
            add_end_marker (bool): if ``True``, point markers are added at the position of the last point (makes easier to track plotting progress).
            update_only_on_visible (bool): ig ``True``, only update plot if the widget is visible.
        """
        self.name=name
        self.setObjectName(self.name)
        self.hLayout=QtWidgets.QVBoxLayout(self)
        self.hLayout.setContentsMargins(0,0,0,0)
        self.hLayout.setObjectName("layout")
        self.plotWidget = pyqtgraph.PlotWidget(self)
        self.plotWidget.setObjectName("plotWidget")
        self.hLayout.addWidget(self.plotWidget)
        self.plotWidget.addLegend()
        self.plotWidget.setLabel("left","Signal")
        self.plotWidget.showGrid(True,True,0.7)

        self.ctl=None
        self.channels={}
        self.channel_indices=[]
        self.data_src_kind=None
        self.data_src=None
        self.add_end_marker=add_end_marker
        self.update_only_on_visible=update_only_on_visible
        self.displayed=[]
        self.vlines=[]
        self.vmarks=[]
    
    def _attach_controller(self, ctl):
        """
        Attach :class:`TracePlotterController` object.

        Called automatically in :meth:`TracePlotterController.setupUi`, doesn't need to be called explicitly.
        """
        self.ctl=ctl


    def setup_channels(self, channels, channel_indices=None):
        """
        Setup and complete plot channels settings (name, color, legend name)
        
        `channels` is a dictionary ``{name: params}``, where ``params`` is a parameter dictionary with the following possible keys:
        ``"name"`` - channel name used in the controller GUI; ``"legend_name"`` - channel name used in the plotting window (legend and x-axis label);
        ``"color"`` - channel plot color; ``"end_marker"`` - overrides global ``end_marker`` property of the plotter;
        ``"factor"`` - rescaling factor applied before plotting.
        """
        self.channels=channels.copy()
        self.channel_indices=channel_indices or sorted(channels.keys())
        mpl_colors=['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#bcbd22','#17becf']
        old_style_colors=['#40FF40','#4040FF','#FF4040','#FFFF00','#00FFFF','#FF00FF','#C0C0C0','#404040']
        colors=(mpl_colors+old_style_colors)*len(channels)
        for idx in self.channel_indices:
            ch=self.channels[idx]
            ch.setdefault("name",idx)
            ch.setdefault("legend_name",ch["name"])
            if "color" not in ch:
                ch["color"]=colors.pop(0)
        if self.ctl:
            self.ctl.setup_channels()
        self._update_plot_lines()



    on_reset=QtCore.pyqtSignal()
    @controller.exsafeSlot()
    def reset_history(self):
        """
        Reset plot history.

        Reset source (if specified) and emits ``on_reset`` signal.
        Automatically called when ``Reset`` controller button is pressed.
        """
        self._reset_data_src()
        self.on_reset.emit()



    def _update_plot_lines(self):
        """
        Update plot lines settings.
        
        Called automatically every time the selection of displayed channels is changed, doesn't need to be called explicitly.
        """
        for el in self.vlines+self.vmarks:
            if el is not None:
                self.plotWidget.plotItem.legend.removeItem(el.name())
                self.plotWidget.removeItem(el)
        self.vlines=[]
        self.vmarks=[]
        for idx in self.displayed:
            ch=self.channels[idx]
            vl=self.plotWidget.plot([],[],pen=ch["color"],name=ch["legend_name"])
            self.vlines.append(vl)
            if ch.get("end_marker",self.add_end_marker):
                vm=self.plotWidget.plot([],[],symbolBrush=ch["color"],symbol="o",symbolSize=5,pxMode=True)
                self.vmarks.append(vm)
            else:
                self.vmarks.append(None)


    def get_enabled_channels(self):
        """Get list of enabled channels and update plot lines if necessary"""
        enabled=self.ctl.get_enabled_channels() if self.ctl else self.channel_indices
        if enabled!=self.displayed:
            self.displayed=enabled
            self._update_plot_lines()
        return enabled
    
    def get_required_channels(self):
        """Get list of channels required for plotting: all enabled channels plus 'X axis' and  'Order by' channels """
        if self.ctl is None:
            return self.channel_indices
        xaxis=self.channel_indices[self.ctl.channels_table.v["xaxis"]]
        order_by=self.channel_indices[self.ctl.channels_table.v["order_by"]]
        return [xaxis,order_by]+self.get_enabled_channels()
    def get_data_from_accum(self, table_accum):
        """
        Get data from the table accumulator, taking selected channels into account
        
        Return dictionary ``{name: column}``.
        """
        channels=self.get_required_channels()
        maxlen=self.ctl.plot_params_table.v["disp_last"] if self.ctl else None
        return table_accum.get_data_dict(channels,maxlen=maxlen,fmt="columns")
    def get_data_from_accum_thread(self, table_accum_thread):
        """
        Get data from the table accumulator thread, taking selected channels into account
        
        Return dictionary ``{name: column}``.
        """
        channels=self.get_required_channels()
        maxlen=self.ctl.plot_params_table.v["disp_last"] if self.ctl else None
        return table_accum_thread.get_data_sync(channels,maxlen=maxlen,fmt="dict")


    def setup_data_source(self, src=None):
        """
        Setup data source.
        
        Add a data source (:class:`.TableAccumulator` or :class:`.TableAccumulatorThread` instance used as a source of data for channels).
        The source is used to automatically grab channel data and receive reset commands.
        Not necessary, if the data is provided explicitly to :meth:`update_plot`.
        """
        if isinstance(src,TableAccumulator):
            self.data_src_kind="accum"
        elif isinstance(src,TableAccumulatorThread):
            self.data_src_kind="accum_thread"
        elif src is None:
            self.data_src_kind=None
        else:
            raise ValueError("unrecognized data source: {}".format(src))
        self.data_src=src
    def get_data_from_source(self):
        """
        Get data from the default source.

        Return dictionary ``{name: column}``.
        """
        if self.data_src_kind=="accum":
            return self.get_data_from_accum(self.data_src)
        elif self.data_src_kind=="accum_thread":
            return self.get_data_from_accum_thread(self.data_src)
    def _reset_data_src(self):
        if self.data_src_kind=="accum":
            return self.data_src.reset_data()
        elif self.data_src_kind=="accum_thread":
            return self.data_src.reset()



    def update_plot(self, data=None, idx_column=None):
        """
        Update plot data.

        Args:
            data: dictionary ``{name: column}`` with the data. Should contain all selected channel and channels used for x-axis and order.
                if not supplied, can be grabbed automatically from the default data source (if supplied).
            idx_column: name of the default index column; if the "order by" column name is the same as `idx_column`, no data re-ordering is performed.
                doesn't need to be supplied, but can improve plotting speed somewhat.
        """
        par=self.ctl.get_all_values() if self.ctl else {"channels/xaxis":0, "channels/order_by":0, "plotting/update_plot":True}
        if par["plotting/update_plot"] and (self.isVisible() or not self.update_only_on_visible):
            if data is None:
                data=self.get_data_from_source()
            xaxis=self.channel_indices[par["channels/xaxis"]]
            order_by=self.channel_indices[par["channels/order_by"]]
            data_channels=[xaxis,order_by]+self.get_enabled_channels()
            norm_data=[]
            for idx in data_channels:
                col=np.asarray(data[idx])
                if "factor" in self.channels[idx]:
                    col=col*self.channels[idx]["factor"]
                norm_data.append(col)
            if norm_data and len(norm_data[0]):
                last_pts=[col[-1] for col in norm_data]
            else:
                last_pts=None
            if order_by!=idx_column:
                norm_data=np.column_stack(norm_data)
                norm_data=waveforms.sort_by(norm_data,x_column=1,stable=True)
                norm_data=[norm_data[:,c] for c in range(norm_data.shape[1])]
            autorange=self.plotWidget.plotItem.getViewBox().autoRangeEnabled()
            self.plotWidget.plotItem.disableAutoRange()
            for vl,col in zip(self.vlines,norm_data[2:]):
                vl.setData(norm_data[0],col)
            if last_pts:
                for vm,pt in zip(self.vmarks,last_pts[2:]):
                    if vm is not None:
                        vm.setData([last_pts[0]],[pt])
            if any(autorange):
                self.plotWidget.plotItem.enableAutoRange(x=autorange[0],y=autorange[1])
            self.plotWidget.setLabel("bottom",self.channels[xaxis]["legend_name"])