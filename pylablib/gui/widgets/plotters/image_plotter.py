"""
PyQtGraph-based image plotter.

Includes additional extensions: pair of lines to extract coordinates, line cuts, settings/getting limits numerically, etc.

Has 2 parts: :class:`ImagePlotter` which displays the image,
and :class:`ImagePlotterCtl` which controls the image display (value ranges, flipping or transposing, etc.)
:class:`ImagePlotter` can also operate alone without a controller.
When both are used, :class:`ImagePlotter` is created and set up first, and then supplied to :meth:`ImagePlotterCtl.setup` method.
"""

from ....core.gui.widgets.param_table import ParamTable
from ....core.gui.widgets.container import QWidgetContainer
from ....core.gui.widgets.layout_manager import QLayoutManagedWidget
from ....core.gui.value_handling import virtual_gui_values
from ....core.thread import controller
from ....core.utils import funcargparse, module, dictionary
from ....core.dataproc import filters, transform

import pyqtgraph

from ....core.gui import QtCore, Signal
import numpy as np
import contextlib
import time
import collections

_pre_0p11=module.cmp_package_version("pyqtgraph","0.11.0")=="<"







class ImagePlotterCtl(QWidgetContainer):
    """
    Class for controlling an image inside :class:`ImagePlotter`.

    Like most widgets, requires calling :meth:`setup` to set up before usage.

    Args:
        parent: parent widget
    """
    def setup(self, plotter, name=None, save_values=("colormap","img_lim_preset")):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Setup the image plotter controller.

        Args:
            name (str): widget name
            plotter (ImagePlotter): controlled image plotter
            save_values (tuple): optional parameters to include on :meth:`get_all_values`;
                can include ``"colormap"`` (colormap defined in the widget), and ``"img_lim_preset"`` (saved image limit preset)
        """
        super().setup(name=name,no_margins=True)
        self.save_values=save_values
        self.setMaximumWidth(200)
        self.plotter=plotter
        self._update_paused=False
        self._update_required={}
        self.params=ParamTable(self)
        self.add_child("params",self.params)
        self.params.setup(add_indicator=False)
        self.img_lim=(None,None)
        self.params.add_text_label("size",label="Image size")
        self.params.add_check_box("flip_x","Flip X",value=False)
        self.params.add_check_box("flip_y","Flip Y",value=False,location=(-1,1))
        self.params.add_check_box("transpose","Transpose",value=True)
        self.params.add_check_box("normalize","Normalize",value=False)
        with self.params.using_new_sublayout("minmaxlim","grid"):
            self.params.add_num_edit("minlim",value=self.img_lim[0],limiter=self.img_lim+("coerce",),formatter=("int"),label="Min",add_indicator=True)
            self.params.add_num_edit("maxlim",value=self.img_lim[1],limiter=self.img_lim+("coerce",),formatter=("int"),label="Max",add_indicator=True)
            self.params.add_spacer(width=30,location=(0,2))
        with self.params.using_new_sublayout("presets","hbox"):
            self.params.add_button("save_preset","Save preset")
            self.params.add_button("load_preset","Load preset")
            @controller.exsafe
            def save_img_lim_preset():
                self.img_lim_preset=self.v["minlim"],self.v["maxlim"]
            @controller.exsafe
            def load_img_lim_preset():
                self.v["minlim"],self.v["maxlim"]=self.img_lim_preset
            self.params.vs["save_preset"].connect(save_img_lim_preset,QtCore.Qt.DirectConnection)
            self.params.vs["load_preset"].connect(load_img_lim_preset,QtCore.Qt.DirectConnection)
            self.img_lim_preset=self.img_lim
        self.params.add_check_box("show_histogram","Show histogram",value=True)
        self.params.add_check_box("auto_histogram_range","Auto histogram range",value=True)
        self.params.add_check_box("show_lines","Show lines",value=True)
        with self.params.using_new_sublayout("system_select","hbox"):
            self.params.add_decoration_label("Use")
            self.params.add_combo_box("coord_system",options={"display":"Display"})
            self.params.add_decoration_label("coordinates")
            self.params.add_padding()
        with self.params.using_new_sublayout("vline","hbox"):
            self.params.add_spacer(width=20)
            self.params.add_check_box("vlineon","X  ",value=True)
            self.params.add_num_edit("vlinepos",value=0,limiter=(0,None,"coerce","float"),formatter=("float","auto",1,True))
        with self.params.using_new_sublayout("hline","hbox"):
            self.params.add_spacer(width=20)
            self.params.add_check_box("hlineon","Y  ",value=True)
            self.params.add_num_edit("hlinepos",value=0,limiter=(0,None,"coerce","float"),formatter=("float","auto",1,True))
        self.params.add_button("center_lines","Center lines")
        self.params.add_check_box("show_linecuts","Show line cuts",value=False)
        self.params.add_num_edit("linecut_width",value=1,limiter=(1,None,"coerce","int"),formatter="int",label="Line cut width")
        self.params.add_spacer(10)
        self.params.add_toggle_button("update_image","Updating",value=True)
        @controller.exsafe
        def arm_single():
            with self._pausing_update(finalize=False):
                self.params.v["update_image"]=False
        self.params.add_button("single","Single").get_value_changed_signal().connect(arm_single,QtCore.Qt.DirectConnection)
        self.params.add_padding()
        def set_img_lim_preset(value):
            self.img_lim_preset=value
        self.add_property_element("img_lim_preset",getter=lambda: self.img_lim_preset,setter=set_img_lim_preset, add_indicator=False)
        def set_colormap(value):
            colormap=dictionary.as_dict(value,style="nested")
            self.plotter.image_window.getHistogramWidget().gradient.restoreState(colormap)
        self.add_property_element("colormap",getter=lambda: self.plotter.image_window.getHistogramWidget().gradient.saveState(),setter=set_colormap,add_indicator=False)  # pylint: disable=unnecessary-lambda
        for n in ["show_histogram","show_lines","vlineon","hlineon","show_linecuts"]:
            self.params.vs[n].connect(self._setup_gui_state,QtCore.Qt.DirectConnection)
        self.params.contained_value_changed.connect(self._on_value_changed,QtCore.Qt.DirectConnection)
        self.plotter._attach_controller(self)
        self._setup_gui_state()

    def set_img_lim(self, *args):
        """
        Set up image value limits.

        Specifies the minimal and maximal values in ``Min`` and ``Max•`` controls.
        Can specify either only upper limit (lower stays the same), or both limits.
        Value of ``None`` implies no limit.
        """
        if len(args)==1:
            self.img_lim=(self.img_lim[0],args[0])
        elif len(args)==2:
            self.img_lim=tuple(args)
        else:
            return
        minl,maxl=self.img_lim
        self.params.w["minlim"].set_limiter((minl,maxl,"coerce"))
        self.params.w["maxlim"].set_limiter((minl,maxl,"coerce"))
    def add_coordinate_system(self, name, label, index=None):
        """Add a new coordinate system label"""
        self.w["coord_system"].insert_option(label,name,index=index)
    @controller.exsafeSlot()
    def _setup_gui_state(self):
        """Enable or disable controls based on which actions are enabled"""
        self.params.set_enabled("auto_histogram_range",self.v["show_histogram"])
        show_lines=self.v["show_lines"]
        self.params.set_enabled(["vlineon","hlineon","show_linecuts"],show_lines)
        self.params.set_enabled("vlinepos",show_lines and self.v["vlineon"])
        self.params.set_enabled("hlinepos",show_lines and self.v["hlineon"])
        self.params.set_enabled("linecut_width",show_lines and self.v["show_linecuts"])
    control_updated=Signal(object)
    @controller.exsafe
    def _on_value_changed(self, name=None, value=None):
        if self._update_paused:
            if name is not None:
                self._update_required[name]=value
        elif self._update_required or name:
            update=self._update_required
            if name is not None:
                update[name]=value
            self._update_required={}
            self.control_updated.emit(update)
    @contextlib.contextmanager
    def _pausing_update(self, finalize=True):
        paused=self._update_paused
        self._update_paused=True
        try:
            yield
        finally:
            self._update_paused=paused
            if finalize:
                self._on_value_changed()
    def set_all_values(self, value):
        with self._pausing_update():
            return super().set_all_values(value)






class EImageItem(pyqtgraph.ImageItem):
    """Minor extension of :class:`pyqtgraph.ImageItem` which keeps track of painting events (last time and number of calls)"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.paint_cnt=0
        self.paint_time=None
        self.allow_repaint=True
    repainted=Signal()
    def paint(self, *args):
        if not self.allow_repaint:
            return
        try:
            self.allow_repaint=False
            self.repainted.emit()
        finally:
            self.allow_repaint=True
        super().paint(*args)
        self.paint_time=time.time()
        self.paint_cnt+=1
    mouse_clicked=Signal(object)
    def mouseClickEvent(self, ev):
        super().mouseClickEvent(ev)
        self.mouse_clicked.emit(ev)
    mouse_dragged=Signal(object)
    def mouseDragEvent(self, ev):
        ev.accept()
        super().mouseDragEvent(ev)
        self.mouse_dragged.emit(ev)
class DummyROI(pyqtgraph.ROI):
    mouse_dragged=Signal(object)
    def mouseDragEvent(self, ev):
        ev.accept()
        self.mouse_dragged.emit(ev)

class EPlotCurveItem(pyqtgraph.PlotCurveItem):
    """Minor extension of :class:`pyqtgraph.PlotCurveItem` which keeps track of painting events (last time and number of calls)"""
    def __init__(self, *args, **kwargs):
        pyqtgraph.PlotCurveItem.__init__(self,*args,**kwargs)
        self.paint_cnt=0
        self.paint_time=None
    def paint(self, *args):
        pyqtgraph.PlotCurveItem.paint(self,*args)
        self.paint_time=time.time()
        self.paint_cnt+=1


builtin_cmaps={ "gray":([0,1.],[(0.,0.,0.),(1.,1.,1.)]),
                "gray_sat":([0,0.99,1.],[(0.,0.,0.),(1.,1.,1.),(1.,0.,0.)]),
                "gray_doublesat":([0,0.01,0.99,1.],[(0.,1.,0.),(0.,0.,0.),(1.,1.,1.),(1.,0.,0.)]),
                "hot":([0,0.3,0.7,1.],[(0.,0.,0.),(1.,0.,0.),(1.,1.,0.),(1.,1.,1.)]),
                "hot_sat":([0,0.3,0.7,0.99,1.],[(0.,0.,0.),(1.,0.,0.),(1.,1.,0.),(1.,1.,1.),(0.,0.,1.)])
            }
try:
    for cm in ["gray_doublesat","hot_sat","hot"]: # add custom cmaps to pyqtgraph widgets
        ticks=[(p,(int(r*255),int(g*255),int(b*255),255)) for p,(r,g,b) in zip(*builtin_cmaps[cm])]
        pyqtgraph.graphicsItems.GradientEditorItem.Gradients[cm]={"ticks":ticks,"mode":"rgb"}
except (TypeError,AttributeError):  # sphinx autodoc Mock can't handle assignment
    pass
TRectangle=collections.namedtuple("TRectangle",["center","size","visible"])
class ImagePlotter(QLayoutManagedWidget):
    """
    Image plotter object.

    Built on top of :class:`pyqtgraph.ImageView` class.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.name=None
        self.ctl=None
        self._virtual_values=self._make_virtual_values()

    lines_updated=Signal()
    frame_selected=Signal(object)
    class Rectangle:
        """
        Describes a rectangle in the plot and its parameters.
        
        Args:
            rect: pyqtgraph rectangle object
        """
        def __init__(self, rect):
            self.rect=rect
            self.center=np.array([0,0])
            self.size=np.array([0,0])
            self.visible=True
            self.coord_system="image"
            self.truncate=False
            self.ignore_bounds=False
        def truncate_to_range(self, center, size):
            """
            Truncate the rectangle to lie within the area given by this center and size.
            
            Return ``True`` if the rectangle parameters were altered and ``False`` otherwise.
            """
            if self.truncate:
                bll=np.array(center)-np.abs(np.array(size))/2
                bur=np.array(center)+np.abs(np.array(size))/2
                ll=self.center-self.size/2
                ur=self.center+self.size/2
                nll=np.sort([bll,ll,bur],axis=0)[1]
                nur=np.sort([bll,ur,bur],axis=0)[1]
                self.center,self.size=(nll+nur)/2,(nur-nll)
                return np.any(nll!=ll) or np.any(nur!=ur)
            return False
        def update(self, center=None, size=None, visible=None, coord_system=None, truncate=None, ignore_bounds=None):
            """
            Update the rectangle with the given parameters
            
            Return ``True`` if any of the parameters were updated and ``False`` otherwise.
            """
            updated=False
            if center is not None and np.any(self.center!=center):
                updated=True
                self.center=np.array(center)
            if size is not None and np.any(self.size!=size):
                updated=True
                self.size=np.array(size)
            if visible is not None and self.visible!=visible:
                updated=True
                self.visible=visible
            if coord_system is not None and self.coord_system!=coord_system:
                updated=True
                self.coord_system=coord_system
            if truncate is not None and self.truncate!=truncate:
                updated=True
                self.truncate=truncate
            if ignore_bounds is not None and self.ignore_bounds!=ignore_bounds:
                updated=True
                self.ignore_bounds=ignore_bounds
            return updated
    class CoordinateSystem:
        """
        Describes a coordinate system.
        
        Args:
            trans: transform connecting this coordinate system to an already defined one
            src: source coordinate system (if ``None``, consider it to be the root system)
            label: coordinate system label (used in the control dropdown menu)
        """
        def __init__(self, trans=None, src=None, label=""):
            self.trans=trans or transform.Indexed2DTransform()
            self.src=src
            self.label=label
        def update(self, trans=None):
            if trans is not None:
                self.trans=trans
        def transform(self):
            """Get the transform which transforms the root coordinates to this system"""
            if self.src is None:
                return self.trans
            return self.trans.preceded(self.src.transform())
    def setup(self, name=None, img_size=(1024,1024), min_size=None):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Setup the image plotter.

        Args:
            name (str): widget name
            img_size (tuple): default image size (used only until actual image is supplied)
            min_size (tuple): minimal widget size (``None`` mean no minimal size)
        """
        super().setup(layout="vbox",no_margins=True)
        self.name=name
        self.single_armed=False
        self.new_image_set=False
        self.img=np.zeros(img_size)
        self.do_image_update=True
        self._ignored_control_variables=set()
        self.xbin=1
        self.ybin=1
        self.dec="mean"
        self._updating_image=False
        self._last_paint_time=None
        self._last_img_paint_cnt=None
        self._last_curve_paint_cnt=[None,None]
        if min_size:
            self.setMinimumSize(QtCore.QSize(*min_size))
        self.image_window=pyqtgraph.ImageView(self,imageItem=EImageItem(image=self.img))
        self.dummy_roi=DummyROI((0,0),(0,0),movable=False,pen="#00000000")
        self.image_window.addItem(self.dummy_roi,ignoreBounds=True)
        self.image_window.getView().sigRangeChanged.connect(lambda _,rng: self._update_dummy_frame(rng),QtCore.Qt.DirectConnection)
        self.add_to_layout(self.image_window)
        self.set_colormap("gray_sat")
        self.image_window.ui.roiBtn.hide()
        self.image_window.ui.menuBtn.hide()
        self.image_window.getView().setMenuEnabled(False)
        self.image_window.getView().setMouseEnabled(x=False,y=False)
        self.image_window.getHistogramWidget().item.vb.setMenuEnabled(False)
        self.vline=pyqtgraph.InfiniteLine(angle=90,movable=True,bounds=[0,None])
        self.hline=pyqtgraph.InfiniteLine(angle=0,movable=True,bounds=[0,None])
        self.image_window.getView().addItem(self.vline)
        self.image_window.getView().addItem(self.hline)
        self.linecut_boundary_pen=pyqtgraph.mkPen("#008000",style=pyqtgraph.QtCore.Qt.DashLine)
        self.hblines=[pyqtgraph.InfiniteLine(angle=0,movable=False,bounds=[0,None],pen=self.linecut_boundary_pen) for _ in range(2)]
        self.vblines=[pyqtgraph.InfiniteLine(angle=90,movable=False,bounds=[0,None],pen=self.linecut_boundary_pen) for _ in range(2)]
        self.image_window.getView().addItem(self.hblines[0])
        self.image_window.getView().addItem(self.hblines[1])
        self.image_window.getView().addItem(self.vblines[0])
        self.image_window.getView().addItem(self.vblines[1])
        self.cut_plot_panel=QLayoutManagedWidget(self)
        self.add_to_layout(self.cut_plot_panel)
        self.cut_plot_panel.setup(layout="vbox",no_margins=True)
        self.cut_plot_window=pyqtgraph.PlotWidget(self.cut_plot_panel)
        self.cut_plot_panel.add_to_layout(self.cut_plot_window)
        self.cut_plot_window.addLegend()
        self.cut_plot_window.setLabel("left","Image cut")
        self.cut_plot_window.showGrid(True,True,0.7)
        self.cut_lines=[EPlotCurveItem(pen="#B0B000",name="Horizontal"),EPlotCurveItem(pen="#B000B0",name="Vertical")]
        for c in self.cut_lines:
            self.cut_plot_window.addItem(c)
        self.cut_plot_panel.setVisible(False)
        self.set_row_stretch([4,1])
        self.vline.sigPositionChanged.connect(lambda: self._update_line_controls(),QtCore.Qt.DirectConnection)  # pylint: disable=unnecessary-lambda
        self.hline.sigPositionChanged.connect(lambda: self._update_line_controls(),QtCore.Qt.DirectConnection)  # pylint: disable=unnecessary-lambda
        self.vline.sigPositionChanged.connect(lambda: self.lines_updated.emit(),QtCore.Qt.DirectConnection)  # pylint: disable=unnecessary-lambda
        self.hline.sigPositionChanged.connect(lambda: self.lines_updated.emit(),QtCore.Qt.DirectConnection)  # pylint: disable=unnecessary-lambda
        self.image_window.getHistogramWidget().sigLevelsChanged.connect(lambda: self._update_levels_controls(self.image_window.getHistogramWidget().getLevels()),QtCore.Qt.DirectConnection)
        @controller.exsafe
        def on_click(ev):
            if ev.double():
                self.set_line_positions(*ev.pos(),coord_system="display")
        self.image_window.imageItem.mouse_clicked.connect(on_click,QtCore.Qt.DirectConnection)
        self.rectangles={}
        self.coord_systems={"display":self.CoordinateSystem(label="Display")}
        self.set_coordinate_system("image",src="display",label="Image")
        self.set_coordinate_system("image_normalized",src="image")
        self._control_coord_system="display"
        self._update_coordinate_systems()
        self.set_rectangle(("special","select_frame"),coord_system="display",color="#00C0C0",ignore_bounds=True,visible=False)
        self._select_frame_state="off"
        self._select_frame_mode="bound"
        self.dummy_roi.mouse_dragged.connect(self._on_frame_drag,QtCore.Qt.DirectConnection)
        self._update_dummy_frame(self.image_window.getView().viewRange())

    def _attach_controller(self, ctl):
        """
        Attach :class:`ImagePlotterCtl` object.

        Called automatically in :meth:`ImagePlotterCtl.setup`
        """
        self.ctl=ctl
        self.ctl.control_updated.connect(self._on_control_update,QtCore.Qt.DirectConnection)
        self._update_coordinate_systems()
        for name,csys in self.coord_systems.items():
            if csys.label is not None and name!="display":
                self.ctl.add_coordinate_system(name,csys.label)
        self.ctl.v["coord_system"]=self._control_coord_system
    def _make_virtual_values(self):
        return virtual_gui_values(**{
                "transpose":False,
                "flip_x":False,
                "flip_y":False,
                "normalize":True,
                "minlim":0,
                "maxlim":1,
                "show_lines":False,
                "vlineon":False,
                "hlineon":False,
                "show_histogram":True,
                "auto_histogram_range":True,
                "show_linecuts":False,
                "vlinepos":0,
                "hlinepos":0,
                "coord_system":"display",
                "linecut_width":1,
                "update_image":True})
    def _get_values(self):
        return self.ctl or self._virtual_values
    def _update_single_variable(self, name, value):
        if name=="update_image":
            self.do_image_update=value
            return {"image"} if value else None
        if name=="center_lines":
            self.center_lines()
            return {"lines"}
        if name=="coord_system" and value!=-1:
            self.set_lines_coordinate_system(value)
            return {"lines"}
        if name=="single":
            self.arm_single()
        if name in {"show_lines","vlineon","hlineon","vlinepos","hlinepos","show_linecuts","linecut_width"}:
            return {"lines"}
        if name in {"transpose","flip_x","flip_y","normalize","minlim","maxlim","show_histogram","auto_histogram_range"}:
            return {"image"}
    @contextlib.contextmanager
    def _ignoring_control_update(self, ignored):
        curr_ignored=self._ignored_control_variables
        self._ignored_control_variables=self._ignored_control_variables|ignored
        try:
            yield
        finally:
            self._ignored_control_variables=curr_ignored
    @controller.exsafe
    def _on_control_update(self, variables):
        to_update=set()
        for k,v in variables.items():
            if k not in self._ignored_control_variables:
                to_update|=self._update_single_variable(k,v) or set()
        if "image" in to_update:
            self.update_image(do_redraw=True)
        elif "lines" in to_update:
            self._update_lines()
    
    @contextlib.contextmanager
    def _while_updating(self, updating=True):
        curr_updating=self._updating_image
        self._updating_image=updating
        try:
            yield
        finally:
            self._updating_image=curr_updating

    def set_colormap(self, cmap):
        """
        Setup colormap.

        Can be name of one built-in colormaps (``"gray"``, ``"gray_sat"``, ``"gray_doublesat"``, ``"hot"``, ``"hot_sat"``),
        one of PyQtGraph built-in cmaps (e.g., ``"flame"`` or ``"bipolar"``),
        a list specifying PyQtGraph colormap or a :class:`pyqtgraph.ColorMap` instance.
        """
        if cmap in pyqtgraph.graphicsItems.GradientEditorItem.Gradients:
            self.image_window.setPredefinedGradient(cmap)
        else:
            cmap=builtin_cmaps.get(cmap,cmap)
            if isinstance(cmap,tuple):
                if any([isinstance(v,float) for c in cmap[1] for v in c]):
                    cols=[tuple([int(v*255) for v in c]) for c in cmap[1]]
                    cmap=cmap[0],cols
                cmap=pyqtgraph.ColorMap(*cmap)
            self.image_window.setColorMap(cmap)
    def set_binning(self, xbin=1, ybin=1, mode="mean", update_image=True):
        """
        Set image binning (useful for showing large images).
        """
        bin_changes=(xbin!=self.xbin) or (ybin!=self.ybin) or (mode!=self.dec)
        self.xbin=xbin
        self.ybin=ybin
        self.dec=mode
        if bin_changes and update_image:
            self.update_image(update_controls=True,do_redraw=True)
    def set_image(self, img):
        """
        Set the current image.

        The image display won't be updated until :meth:`update_image` is called.
        This function is thread-safe (i.e., the application state remains consistent if it's called from another thread,
        although race conditions on simultaneous calls from multiple threads still might happen).
        """
        if self.do_image_update or self.single_armed:
            img=np.asarray(img)
            if img.ndim!=2 or (img.ndim==3 and img.shape[2] not in (3,4)):
                raise ValueError("only 2D images or 3D images with 3 or 4 color channels are allowed; got image with the shape {}".format(img.shape))
            self.img=img
            self.single_armed=False
            self.new_image_set=True
    def arm_single(self):
        """Arm the single-image trigger"""
        self.single_armed=True

    def _show_histogram(self, show=True):
        if show:
            self.image_window.ui.histogram.show()
        else:
            self.image_window.ui.histogram.hide()
    def _update_coordinate_systems(self):
        values=self._get_values()
        imshape=self.img.shape
        dimshape=imshape
        im2disp=transform.Indexed2DTransform()
        im2disp=im2disp.multiplied([1/self.xbin,1/self.ybin])
        if values.v["transpose"]:
            im2disp=im2disp.multiplied([[0,1],[1,0]])
            dimshape=dimshape[::-1]
        if values.v["flip_x"]:
            im2disp=im2disp.multiplied([-1,1]).shifted([dimshape[0],0])
        if values.v["flip_y"]:
            im2disp=im2disp.multiplied([1,-1]).shifted([0,dimshape[1]])
        self.coord_systems["image"].update(im2disp.inverted())
        im2norm=transform.Indexed2DTransform().multiplied([1/imshape[0],1/imshape[1]])
        self.coord_systems["image_normalized"].update(im2norm)
    def _convert_coordinates(self, coord, src="display", dst="display"):
        if src!="display":
            strans=self.coord_systems[src].transform()
            coord=strans.i(coord)
        if dst!="display":
            dtrans=self.coord_systems[dst].transform()
            coord=dtrans(coord)
        return tuple(coord)
    def _convert_rectangle(self, center, size, src="display", dst="display"):
        ll=np.array(self._convert_coordinates(np.asarray(center)-np.asarray(size)/2,src=src,dst=dst))
        ur=np.array(self._convert_coordinates(np.asarray(center)+np.asarray(size)/2,src=src,dst=dst))
        center=(ll+ur)/2
        size=np.abs(ll-ur)
        return center,size
    def set_coordinate_system(self, name, trans=None, src="display", label=None):
        """
        Add or change parameters of a coordinate system with a given name.
        
        `trans` specifies a transform (involves shifts, scales, multiples of 90-degree rotation, and mirrors)
        relative to the source coordinate system (can only be set on creation and not changed later).
        By default, coordinate systems ``"display"`` (display coordinates, x-y order), ``"image"`` (image coordinates, row-column order),
        and ``"image_normalized"`` (same as image rescaled to be between 0 and 1) are defined.
        """
        if name not in self.coord_systems:
            self.coord_systems[name]=self.CoordinateSystem(trans=trans,src=self.coord_systems[src],label=label)
            if self.ctl is not None and label is not None:
                self.ctl.add_coordinate_system(name,label=label)
        else:
            self.coord_systems[name].update(trans=trans)
    def set_rectangle(self, name, center=None, size=None, visible=None, color=None, coord_system=None, truncate=None, ignore_bounds=None):
        """
        Add or change parameters of a rectangle with a given name.

        Any parameters equal to ``None`` stay unchanged, unless the rectangle is first created, in which case the default parameters are used.
        Rectangle `center` and `size` are specified in the coordinate system given by `coord_system` (``"image"`` by default).
        `visible` shows and hides the rectangle, and `color` specifies its color; by default the rectangle is visible upon creation and has magenta color.
        If ``truncate==True``, then its extent is automatically truncated to the image region (``False`` by default).
        If ``ignore_bounds==True``, then the rectangle does not affect the display bounds (``False`` by default).
        """
        if name not in self.rectangles:
            pqrect=pyqtgraph.ROI((0,0),(0,0),movable=False,pen=color or "#FF00FF")
            self.rectangles[name]=self.Rectangle(pqrect)
        else:
            if color is not None:
                self.rectangles[name].pqrect.setPen(color)
        rect=self.rectangles[name]
        updated=rect.update(center,size,visible=visible,coord_system=coord_system,truncate=truncate,ignore_bounds=ignore_bounds)
        img_shape=self._get_draw_img_shape()
        imcenter,imsize=self._convert_rectangle(np.array(img_shape)/2,np.array(img_shape),dst=rect.coord_system)
        updated=rect.truncate_to_range(imcenter,imsize) or updated
        center,size=self._convert_rectangle(rect.center,rect.size,src=rect.coord_system)
        updated=updated or np.any(rect.rect.pos()!=(center-size/2)) or np.any(rect.rect.size()!=size)
        if updated:
            rect.rect.setPos(center-size/2)
            rect.rect.setSize(size)
            imgview=self.image_window.getView()
            if rect.visible and rect.rect not in imgview.scene().items():
                imgview.addItem(rect.rect,ignoreBounds=rect.ignore_bounds)
            elif not rect.visible and rect.rect in imgview.scene().items():
                imgview.removeItem(rect.rect)
        return updated
    def update_rectangles(self):
        """Update rectangle coordinates"""
        for name in self.rectangles:
            self.set_rectangle(name)
    def del_rectangle(self, name):
        """Delete a rectangle with a given name"""
        if name in self.rectangles:
            rect=self.rectangles.pop(name)
            self.image_window.getView().removeItem(rect.rect)
    def _get_rect_names(self, names, include_special=False):
        if names is None:
            return [n for n in self.rectangles if include_special or not (isinstance(n,tuple) and n[0]=="special")]
        return [n for n in funcargparse.as_sequence(names) if n in self.rectangles]
    def show_rectangles(self, show=True, names=None):
        """
        Toggle showing rectangles on or off
        
        If `names` is given, it specifies names of rectangles to show or hide (by default, all rectangles).
        """
        names=self._get_rect_names(names)
        return any([self.set_rectangle(n,visible=show) for n in names])
    def get_rectangles(self, names=None, coord_system="image", include_special=False):
        """
        Get a dictionary of rectangle properties.
        
        Return dictionary of tuple ``(center, size, visible)``.
        `coord_system` specifies the coordinate system for the positions and sizes.
        If ``include_special==True``, include special rectangles such as selection frame.
        """
        names=self._get_rect_names(names,include_special=include_special)
        rects=[self.rectangles[n] for n in names]
        geom=[self._convert_rectangle(r.center,r.size,src=r.coord_system,dst=coord_system) for r in rects]
        return {n:TRectangle(g[0],g[1],r.visible) for n,r,g in zip(names,rects,geom)}
    @controller.exsafe
    def _update_dummy_frame(self, rng):
        (l,r),(b,t)=rng
        pad=5
        self.dummy_roi.setPos((l-pad,b-pad))
        self.dummy_roi.setSize((r-l+pad*2,t-b+pad*2))
    @controller.exsafe
    def _on_frame_drag(self, ev):
        if self._select_frame_state=="off":
            return
        pref=np.array(self.dummy_roi.pos())
        p1=np.array(ev.buttonDownPos())+pref
        p2=np.array(ev.pos())+pref
        if ev.isStart() and self._select_frame_mode=="image":
            if np.any(p1<0) or np.any(p1>self._get_draw_img_shape()):
                return
        self.set_rectangle(("special","select_frame"),(p1+p2)/2,np.abs(p1-p2))
        if ev.isStart():
            self._select_frame_state="active" if self._select_frame_state=="idle" else "single"
            self.set_rectangle(("special","select_frame"),visible=True)
        if self._select_frame_state not in ["active","single"]:
            return
        if ev.isFinish():
            self._select_frame_state="idle" if self._select_frame_state=="active" else "off"
            self.set_rectangle(("special","select_frame"),visible=False)
            self.frame_selected.emit(self.get_selection_frame())
    def enable_selection_frame(self, enable=True, single=False, image_bound=True):
        """
        Enable or disable selection frame mode.

        If enabled, dragging using left mouse button shows a selection frame.
        When done, it send ``frame_selected`` message with the frame in the ``image`` coordinates as ``(start_corner, end_corner)``
        (:meth:`get_selection_frame` can be used to get it in other coordinates).
        If ``single==True``, the selection mode is automatically turned off after a single selection.
        If ``image_bound==True``, the frame is bound to the image region; otherwise, it can be drawn anywhere.
        """
        if enable:
            if self._select_frame_state not in ["active","single"]:
                self._select_frame_state="idle_single" if single else "idle"
                self.set_rectangle(("special","select_frame"),truncate=image_bound)
                self._select_frame_mode="image" if image_bound else "full"
        else:
            self._select_frame_state="off"
            self.set_rectangle(("special","select_frame"),center=(0,0),size=(0,0),visible=False)
    def get_selection_frame(self, coord_system="image"):
        """Get selection frame coordinates as a tuple ``(start_corner, end_corner)``"""
        rect=self.rectangles[("special","select_frame")]
        p1,p2=rect.center-rect.size/2,rect.center+rect.size/2
        return tuple(np.array(self._convert_coordinates(p,dst=coord_system)) for p in [p1,p2])

    def set_lines_coordinate_system(self, coord_system):
        """Set a different coordinate system for the lines GUI control"""
        if coord_system!=self._control_coord_system:
            self._control_coord_system=coord_system
            with self._ignoring_control_update({"coord_system"}):
                self._get_values().v["coord_system"]=coord_system
            self._update_line_controls()
    @controller.exsafe
    def center_lines(self):
        """Center coordinate lines"""
        self.set_line_positions(0.5,0.5,"image_normalized")
    def get_line_positions(self, coord_system="image"):
        """Return lines positions referenced to the given coordinate system"""
        values=self._get_values()
        if not values.v["show_lines"] or self.img is None:
            return None
        ipos,jpos=values.v["vlinepos"],values.v["hlinepos"]
        return self._convert_coordinates((ipos,jpos),src=self._control_coord_system,dst=coord_system)
    def set_line_positions(self, ipos=None, jpos=None, coord_system="image"):
        """Set line positions referenced to the given coordinate system"""
        if self.img is None:
            return None
        if ipos is None or jpos is None:
            cipos,cjpos=self.get_line_positions(coord_system=coord_system)
            ipos=cipos if ipos is None else ipos
            jpos=cjpos if jpos is None else jpos
        vpos,hpos=self._convert_coordinates((ipos,jpos),src=coord_system)
        self.vline.setPos(vpos)
        self.hline.setPos(hpos)
    def _update_linecut_boundaries(self, values):
        vpos=self.vline.getPos()[0]
        hpos=self.hline.getPos()[1]
        cut_width=values.v["linecut_width"]
        show_boundary_lines=values.v["show_lines"] and values.v["show_linecuts"] and cut_width>1
        for ln in self.vblines:
            ln.setPen(self.linecut_boundary_pen if show_boundary_lines and values.v["vlineon"] else None)
        for ln in self.hblines:
            ln.setPen(self.linecut_boundary_pen if show_boundary_lines and values.v["hlineon"] else None)
        if show_boundary_lines:
            vbin,hbin=(self.xbin,self.ybin) if not values.v["transpose"] else (self.ybin,self.xbin)
            self.vblines[0].setPos(vpos-cut_width*vbin/2)
            self.vblines[1].setPos(vpos+cut_width*vbin/2)
            self.hblines[0].setPos(hpos-cut_width*hbin/2)
            self.hblines[1].setPos(hpos+cut_width*hbin/2)

    # Update image controls based on PyQtGraph image window
    @controller.exsafe
    def _update_levels_controls(self, levels):
        values=self._get_values()
        with self._ignoring_control_update({"minlim","maxlim"}):
            values.v["minlim"],values.v["maxlim"]=levels
    @controller.exsafe
    def _update_line_controls(self):
        values=self._get_values()
        with self._ignoring_control_update({"vlinepos","hlinepos"}):
            vpos,hpos=self.vline.getPos()[0],self.hline.getPos()[1]
            ipos,jpos=self._convert_coordinates((vpos,hpos),dst=self._control_coord_system)
            values.v["vlinepos"]=ipos
            values.v["hlinepos"]=jpos
        self._update_linecut_boundaries(values)
    def _sanitize_img(self, img): # PyQtGraph histogram has an unfortunate failure mode (crashing) when the image is integer and is constant
        """Correct the image so that it doesn't cause crashes on pyqtgraph 0.10.0"""
        if not _pre_0p11:
            return img
        if np.prod(img.shape)<=1: # empty or single-pixel image
            img=np.zeros((2,2),dtype=img.dtype)+(img[0,0] if np.prod(img.shape) else 0)
        step=int(np.ceil(img.shape[0]/200)),int(np.ceil(img.shape[1]/200))
        stepData=img[::step[0],::step[1]]
        if stepData.dtype.kind in "ui" and stepData.min()==stepData.max():
            img=img.copy()
            img[0,0]+=1
        return img
    def _check_paint_done(self, dt=0):
        items=[self.image_window.imageItem]+self.cut_lines
        counters=[self._last_img_paint_cnt]+self._last_curve_paint_cnt
        if self._last_img_paint_cnt==self.image_window.imageItem.paint_cnt:
            return False
        for itm,cnt in zip(items,counters):
            if itm.paint_cnt==cnt:
                return False
        t=time.time()
        passed_time=min([t-(itm.paint_time or 0) for itm in items])
        if passed_time<dt:
            return False
        return True
    # Update image plot
    def _get_draw_img(self):
        values=self._get_values()
        draw_img=self.img
        if self.xbin>1:
            draw_img=filters.decimate(draw_img,self.xbin,dec=self.dec,axis=0)
        if self.ybin>1:
            draw_img=filters.decimate(draw_img,self.ybin,dec=self.dec,axis=1)
        if values.v["transpose"]:
            draw_img=draw_img.transpose()
        if values.v["flip_x"]:
            draw_img=draw_img[::-1,:]
        if values.v["flip_y"]:
            draw_img=draw_img[:,::-1]
        return draw_img
    def _get_draw_img_shape(self):
        shape=np.array(self.img.shape)
        values=self._get_values()
        shape//=[self.xbin,self.ybin]
        if values.v["transpose"]:
            shape=shape[::-1]
        return shape
    def _update_lines(self, draw_img=None):
        values=self._get_values()
        if draw_img is None:
            draw_img=self._get_draw_img()
        show_lines=values.v["show_lines"]
        vlineon,hlineon=values.v["vlineon"],values.v["hlineon"]
        ipos,jpos=values.v["vlinepos"],values.v["hlinepos"]
        for ln,lnena in zip([self.vline,self.hline],[vlineon,hlineon]):
            ln.setPen("g" if show_lines and lnena else None)
            ln.setHoverPen("y" if show_lines and lnena else None)
            ln.setMovable(show_lines and lnena)
        for ln in [self.vline]+self.vblines:
            ln.setBounds([0,draw_img.shape[0]])
        for ln in [self.hline]+self.hblines:
            ln.setBounds([0,draw_img.shape[1]])
        with self._ignoring_control_update({"vlinepos","hlinepos"}):
            self.set_line_positions(ipos,jpos,coord_system=self._control_coord_system)
        self._update_linecut_boundaries(values)
        if self.isVisible():
            if values.v["show_lines"] and values.v["show_linecuts"]:
                vpos,hpos=self.get_line_positions(coord_system="display")
                cut_width=values.v["linecut_width"]
                vmin=int(min(max(0,vpos-cut_width/2),draw_img.shape[0]-1))
                vmax=int(vpos+cut_width/2)
                if vmax==vmin:
                    if vmin==0:
                        vmax+=1
                    else:
                        vmin-=1
                hmin=int(min(max(0,hpos-cut_width/2),draw_img.shape[1]-1))
                hmax=int(hpos+cut_width/2)
                if hmax==hmin:
                    if hmin==0:
                        hmax+=1
                    else:
                        hmin-=1
                x_cut=draw_img[:,hmin:hmax].mean(axis=1) if hlineon else []
                y_cut=draw_img[vmin:vmax,:].mean(axis=0) if vlineon else []
                autorange=self.cut_plot_window.getViewBox().autoRangeEnabled()
                self.cut_plot_window.disableAutoRange()
                self.cut_lines[0].setData(np.arange(len(x_cut)),x_cut)
                self.cut_lines[1].setData(np.arange(len(y_cut)),y_cut)
                self._last_img_paint_cnt=[cl.paint_cnt for cl in self.cut_lines]
                if any(autorange):
                    self.cut_plot_window.enableAutoRange(x=autorange[0],y=autorange[1])
                self.cut_plot_panel.setVisible(True)
            else:
                self.cut_plot_panel.setVisible(False)
    def update_expected(self, do_redraw=False, only_new_image=True):
        """
        Check if the subsequent :meth:`update_image` call is expected to lead to an image update.

        All arguments are the same as in :meth:`update_image`.
        """
        if self._updating_image:
            return False
        dt=min(time.time()-self._last_paint_time,0.1) if self._last_paint_time else 0.1
        if not self._check_paint_done(dt*0.1):
            return False
        if not do_redraw:
            if not self.new_image_set and (only_new_image or not self.do_image_update):
                return False
        return self.isVisible()
    @controller.exsafe
    def update_image(self, update_controls=True, do_redraw=False, only_new_image=True):
        """
        Update displayed image.

        If ``update_controls==True``, update control values (such as image min/max values and line positions); otherwise, keep the current values.
        If ``do_redraw==True``, force update regardless of the ``"update_image"`` button state; otherwise, update only if it is enabled.
        If ``only_new_image==True`` and the image hasn't changed since the last call to ``update_image``, skip redraw (however, if ``do_redraw==True``, force redrawing regardless).
        """
        if self._updating_image:
            return
        dt=min(time.time()-self._last_paint_time,0.1) if self._last_paint_time else 0.1
        if not self._check_paint_done(dt*0.1) and not do_redraw:
            return
        with self._while_updating():
            values=self._get_values()
            if not do_redraw:
                if not self.new_image_set and (only_new_image or not self.do_image_update):
                    return
            self.new_image_set=False
            draw_img=self._get_draw_img()
            img_levels=[0,1] if np.all(np.isnan(draw_img)) else (np.nanmin(draw_img),np.nanmax(draw_img))
            autoscale=values.v["normalize"]
            levels=img_levels if autoscale else (values.v["minlim"],values.v["maxlim"])
            draw_img=self._sanitize_img(draw_img)
            self._update_coordinate_systems()
            self.update_rectangles()
            self._update_lines(draw_img=draw_img)
            if self.isVisible():
                self.image_window.setImage(draw_img,levels=levels,autoHistogramRange=False)
                if values.v["auto_histogram_range"] or all(self.image_window.ui.histogram.vb.autoRangeEnabled()):
                    hist_range=min(img_levels[0],levels[0]),max(img_levels[1],levels[1])
                    if hist_range[0]==hist_range[1]:
                        hist_range=hist_range[0]-.5,hist_range[1]+.5
                    self.image_window.ui.histogram.setHistogramRange(*hist_range)
                self._last_img_paint_cnt=self.image_window.imageItem.paint_cnt
            if update_controls:
                if autoscale:
                    self._update_levels_controls(levels)
                self._update_line_controls()
            self._show_histogram(values.v["show_histogram"])
            values.i["minlim"]=img_levels[0]
            values.i["maxlim"]=img_levels[1]
            values.v["size"]="{} x {}".format(*draw_img.shape)
            self._last_paint_time=time.time()
            return values






class ImagePlotterCombined(QWidgetContainer):
    """
    A combined panel which includes :class:`ImagePlotter` and :class:`ImagePlotterCtl` in the sidebar.

    The :meth:`setup` method takes parameters both for plotter and controller setup.
    In addition, it takes ``ctl_caption`` argument, which, if not ``None``, sets the caption of a group box made around the controller panel.
    The plotter can be accessed as ``.plt`` attribute, and the controller as ``.ctl`` attribute.
    The ``"sidebar"`` sublayout can be used to add additional elements if necessary.
    """
    def setup(self, img_size=(1024,1024), min_size=None, ctl_caption=None, name=None, save_values=("colormap","img_lim_preset")):  # pylint: disable=arguments-differ, arguments-renamed
        super().setup(layout="hbox",name=name)
        self.plt=ImagePlotter(self)
        self.add_to_layout(self.plt)
        self.plt.setup(name="plt",img_size=img_size,min_size=min_size)
        with self.using_new_sublayout("sidebar","vbox"):
            self.ctl=ImagePlotterCtl(self)
            if ctl_caption is None:
                self.add_child("ctl",self.ctl)
            else:
                self.add_group_box("ctl_box",caption=ctl_caption).add_child("ctl",self.ctl)
                self.c["ctl_box"].setFixedWidth(200)
            self.ctl.setup(self.plt,save_values=save_values)
            self.add_padding()
        self.get_sublayout().setStretch(0,1)