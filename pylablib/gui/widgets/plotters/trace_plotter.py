"""
PyQtGraph-based trace plotter.

Has 2 parts: :class:`TracePlotter` which displays the plots,
and :class:`TracePlotterCtl` which controls the channels (X-axis, enabled channels) and the plotting (buffer size, updating, etc.)
:class:`TracePlotter` can also operate alone without a controller.
When both are used, :class:`TracePlotter` is created and set up first, and then supplied to :meth:`TracePlotterCtl.setup` method.
"""

from ....core.gui.widgets.param_table import ParamTable
from ....core.gui.widgets.container import QWidgetContainer
from ....core.gui.widgets.layout_manager import QLayoutManagedWidget
from ....core.thread import controller
from ....core.dataproc import utils as trace_utils
from ....thread.stream.table_accum import TableAccumulator, TableAccumulatorThread

import pyqtgraph

from ....core.gui import QtCore, Signal
import numpy as np
import collections


class TracePlotterCtl(QWidgetContainer):
    """
    Class for controlling traces inside :class:`TracePlotter`.

    Like most widgets, requires calling :meth:`setup` to set up before usage.

    Args:
        parent: parent widget
    """
    def setup(self, plotter, name=None):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Setup the trace plotter controller.

        Args:
            name (str): widget name
            plotter (TracePlotter): controlled image plotter
        """
        super().setup(name=name,no_margins=True)
        self.plotter=plotter
        self.plotter._attach_controller(self)
        self.channels_table=ParamTable(self)
        self.add_group_box("channels_box",caption="Channels").add_child("channels",self.channels_table,gui_values_path="channels")
        self.channels_table.setMinimumSize(QtCore.QSize(20,20))
        self.channels_table.setup(add_indicator=False)
        self.channels_table.contained_value_changed.connect(self.channels_updated)
        self.setup_channels()
        self.plot_params_table=ParamTable(self)
        self.add_group_box("plotting_box",caption="Plotting").add_child("plotting",self.plot_params_table,gui_values_path="plotting")
        self.plot_params_table.setMinimumSize(QtCore.QSize(20,20))
        self.plot_params_table.setup(add_indicator=False)
        self.plot_params_table.add_toggle_button("update_plot","Updating")
        self.plot_params_table.add_num_edit("disp_last",1,limiter=(1,None,"coerce","int"),formatter=("int"),label="Display last: ")
        self.plot_params_table.add_button("reset_history","Reset").get_value_changed_signal().connect(self.plotter.reset_history)
        self.add_padding()
        self.main_layout.setStretch(2,1)

    channels_updated=Signal(object,object)
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






mpl_colors=['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#bcbd22','#17becf']
old_style_colors=['#40FF40','#4040FF','#FF4040','#FFFF00','#00FFFF','#FF00FF','#C0C0C0','#404040']
all_colors=mpl_colors+old_style_colors
class TracePlotter(QLayoutManagedWidget):
    """
    Trace plotter object.

    Built on top of :class:`.pyqtgraph.PlotWidget` class.

    Intended for plotting of gradually-accumulated data;
    designed to work tightly with :class:`.TableAccumulator` or :class:`.TableAccumulatorThread` as data sources.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.name=None
        self.ctl=None
    def setup(self, name=None, add_end_marker=False, update_only_on_visible=True, full_data=False):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Setup the image view.

        Args:
            name (str): widget name
            add_end_marker (bool): if ``True``, point markers are added at the position of the last point (makes easier to track plotting progress).
            update_only_on_visible (bool): if ``True``, only update plot if the widget is visible.
            full_data (bool): if ``True``, whenever data is updated from the source, all channels are requested and stored;
                this makes it a bit more CPU and memory-heavy, but allows reconfiguring the plot while paused
        """
        self.name=name
        super().setup(layout="vbox",no_margins=True)
        self.plot_widget=pyqtgraph.PlotWidget(self)
        self.add_to_layout(self.plot_widget)
        self.plot_widget.addLegend()
        self.plot_widget.setLabel("left","Signal")
        self.plot_widget.showGrid(True,True,0.7)

        self.ctl=None
        self.channels={}
        self.channel_indices=[]
        self.data_src_kind=None
        self.data_src=None
        self.add_end_marker=add_end_marker
        self.update_only_on_visible=update_only_on_visible
        self.full_data=full_data
        self.displayed=[]
        self.vlines=[]
        self.vmarks=[]
        self._drag_lines={}
        self._plotted_data=None
    
    def _attach_controller(self, ctl):
        """
        Attach :class:`TracePlotterCtl` object.

        Called automatically in :meth:`TracePlotterCtl.setup`, doesn't need to be called explicitly.
        """
        if self.ctl is not None and self.ctl is not ctl:
            raise RuntimeError("a different controller is already attached")
        self.ctl=ctl
        self.ctl.channels_updated.connect(controller.exsafe(lambda: self._draw_plot()))  # pylint: disable=unnecessary-lambda
        @controller.exsafe
        def update_lines(name, _):
            if name=="xaxis":
                self._update_drag_lines()
        self.ctl.channels_updated.connect(update_lines)


    def setup_channels(self, channels, channel_indices=None):
        """
        Setup and complete plot channels settings (name, color, legend name)
        
        `channels` is a dictionary ``{name: params}``, where ``params`` is a parameter dictionary with the following possible keys:
        ``"name"`` - channel name used in the controller GUI; ``"legend_name"`` - channel name used in the plotting window (legend and x-axis label);
        ``"color"`` - channel plot color; ``"end_marker"`` - overrides global ``end_marker`` property of the plotter;
        ``"factor"`` - rescaling factor applied before plotting.
        """
        self.channels=channels.copy()
        self.channel_indices=channel_indices or list(channels.keys())
        colors=all_colors*len(channels)
        for idx in self.channel_indices:
            ch=self.channels[idx]
            ch.setdefault("name",idx)
            ch.setdefault("legend_name",ch["name"])
            if "color" not in ch:
                ch["color"]=colors.pop(0)
        if self.ctl:
            self.ctl.setup_channels()
        self._update_plot_lines()



    on_reset=Signal()
    @controller.exsafeSlot()
    def reset_history(self):
        """
        Reset plot history.

        Reset source (if specified) and emits ``on_reset`` signal.
        Automatically called when ``Reset`` controller button is pressed.
        """
        self._reset_data_src()
        self.on_reset.emit()


    TDragLine=collections.namedtuple("TDragLine",["channels","positions","line"])
    def add_vertical_line(self, name, channels="all"):
        """
        Add a draggable vertical line to the plot.

        `channels` can specify x-axis channels for which this line is visible (``"all"`` means all channels).
        """
        if name in self._drag_lines:
            raise ValueError("line {} already exists".format(name))
        line=pyqtgraph.InfiniteLine(angle=90,movable=True)
        line.setZValue(20)
        self.plot_widget.getPlotItem().getViewBox().addItem(line,ignoreBounds=True)
        self._drag_lines[name]=self.TDragLine(channels,{},line)
        line.sigPositionChanged.connect(self._make_line_updater(name),QtCore.Qt.DirectConnection)
        self._update_drag_lines()
    def _make_line_updater(self, name):
        @controller.exsafe
        def update():
            xaxis=self.ctl.v["channels/xaxis"] if self.ctl else 0
            self._drag_lines[name].positions[xaxis]=self._drag_lines[name].line.getPos()[0]
        return update
    def _update_drag_lines(self, par=None):
        if par is None:
            xaxis=self.ctl.v["channels/xaxis"] if self.ctl else 0
        else:
            xaxis=par["channels/xaxis"]
        for dln in self._drag_lines.values():
            if dln.channels=="all" or self.channel_indices[xaxis] in dln.channels:
                visible=True
                if xaxis in dln.positions:
                    dln.line.setPos(dln.positions[xaxis])
            else:
                visible=False
            dln.line.setPen("g" if visible else None)
            dln.line.setHoverPen("y" if visible else None)
            dln.line.setMovable(visible)
    def is_line_visible(self, name):
        """Check if the line with the given name is visible"""
        return self._drag_lines[name].line.movable
    def get_line_position(self, name, channel=None, only_visible=True):
        """
        Get the position of a line with the given name for a given channel.

        If `channel` is ``None``, use the current x-axis channel.
        If ``only_visible==True`` and the line is currently invisible, return ``None``.
        """
        if only_visible and not self.is_line_visible(name):
            return None
        if channel is None:
            channel=self.ctl.v["channels/xaxis"]
        else:
            channel=self.channel_indices.index(channel)
        return self._drag_lines[name].positions.get(channel,None)
    def set_line_position(self, name, position, channel=None, only_visible=True):
        """
        Set the position of a line with the given name for a given channel.

        If `channel` is ``None``, use the current x-axis channel.
        If ``only_visible==True`` and the line is currently invisible, do nothing.
        """
        if only_visible and not self.is_line_visible(name):
            return
        xaxis=self.ctl.v["channels/xaxis"]
        if channel is None:
            channel=xaxis
        else:
            channel=self.channel_indices.index(channel)
        if channel==xaxis:
            self._drag_lines[name].line.setPos(position)
        else:
            self._drag_lines[name].positions[channel]=position
    def center_line(self, name, only_visible=True):
        """
        Center line with the given name within the plot range.

        If ``only_visible==True`` and the line is currently invisible, do nothing.
        """
        if only_visible and not self.is_line_visible(name):
            return
        rng=self.plot_widget.getAxis("bottom").range
        self._drag_lines[name].line.setPos((rng[0]+rng[1])/2)


    def _update_plot_lines(self):
        """
        Update plot lines settings.
        
        Called automatically every time the selection of displayed channels is changed, doesn't need to be called explicitly.
        """
        for el in self.vlines+self.vmarks:
            if el is not None:
                self.plot_widget.plotItem.legend.removeItem(el.name())
                self.plot_widget.removeItem(el)
        self.vlines=[]
        self.vmarks=[]
        for idx in self.displayed:
            ch=self.channels[idx]
            vl=self.plot_widget.plot([],[],pen=ch["color"],name=ch["legend_name"])
            self.vlines.append(vl)
            if ch.get("end_marker",self.add_end_marker):
                vm=self.plot_widget.plot([],[],symbolBrush=ch["color"],symbol="o",symbolSize=5,pxMode=True)
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
        if self.ctl is None or self.full_data:
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
        return table_accum_thread.csi.get_data(channels,maxlen=maxlen,fmt="dict")


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


    def _draw_plot(self, data=None, par=None, idx_column=None):
        """
        Draw the plot using the given data, parameters dictionary, and index column.
        
        If data is not supplied, use the last plotted data (if none is available, do nothing).
        """
        if data is None:
            data=self._plotted_data
        if data is None:
            return
        if self.full_data:
            self._plotted_data=data
        if par is None:
            par=self.ctl.get_all_values() if self.ctl else {"channels/xaxis":0, "channels/order_by":0, "plotting/update_plot":True}
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
            norm_data=trace_utils.sort_by(norm_data,x_column=1,stable=True)
            norm_data=[norm_data[:,c] for c in range(norm_data.shape[1])]
        autorange=self.plot_widget.plotItem.getViewBox().autoRangeEnabled()
        self.plot_widget.plotItem.disableAutoRange()
        for vl,col in zip(self.vlines,norm_data[2:]):
            vl.setData(norm_data[0],col)
        if last_pts:
            for vm,pt in zip(self.vmarks,last_pts[2:]):
                if vm is not None:
                    vm.setData([last_pts[0]],[pt])
        if any(autorange):
            self.plot_widget.plotItem.enableAutoRange(x=autorange[0],y=autorange[1])
        self.plot_widget.setLabel("bottom",self.channels[xaxis]["legend_name"])
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
            self._draw_plot(data=data,par=par,idx_column=idx_column)
            






class TracePlotterCombined(QWidgetContainer):
    """
    A combined panel which includes :class:`TracePlotter` and :class:`TracePlotterCtl` in the sidebar.

    The :meth:`setup` method takes parameters both for plotter and controller setup.
    The plotter can be accessed as ``.plt`` attribute, and the controller as ``.ctl`` attribute.
    The ``"sidebar"`` sublayout can be used to add additional elements if necessary.
    """
    def setup(self, add_end_marker=False, update_only_on_visible=True, full_data=False, name=None):  # pylint: disable=arguments-differ, arguments-renamed
        super().setup(layout="hbox",no_margins=True,name=name)
        self.plt=TracePlotter(self)
        self.add_to_layout(self.plt)
        self.plt.setup(name="plt",add_end_marker=add_end_marker,update_only_on_visible=update_only_on_visible,full_data=full_data)
        with self.using_new_sublayout("sidebar","vbox"):
            self.ctl=TracePlotterCtl(self)
            self.add_child("ctl",self.ctl)
            self.ctl.setup(self.plt)
            self.add_padding()
        self.get_sublayout().setStretch(0,1)