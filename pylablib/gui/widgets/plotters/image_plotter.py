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
from ....core.dataproc import filters

import pyqtgraph

from ....core.gui import QtCore, Signal
import numpy as np
import contextlib
import time

_pre_0p11=module.cmp_package_version("pyqtgraph","0.11.0")=="<"







class ImagePlotterCtl(QWidgetContainer):
    """
    Class for controlling an image inside :class:`ImagePlotter`.

    Like most widgets, requires calling :meth:`setup` to set up before usage.

    Args:
        parent: parent widget
    """
    def setup(self, plotter, name=None, save_values=("colormap","img_lim_preset")):  # pylint: disable=arguments-differ
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
        self.plotter._attach_controller(self)
        self.params=ParamTable(self)
        self.add_child("params",self.params)
        self.params.setup(add_indicator=False)
        self.img_lim=(None,None)
        self.params.add_text_label("size",label="Image size:")
        self.params.add_check_box("flip_x","Flip X",value=False)
        self.params.add_check_box("flip_y","Flip Y",value=False,location=(-1,1))
        self.params.add_check_box("transpose","Transpose",value=True)
        self.params.add_check_box("normalize","Normalize",value=False)
        with self.params.using_new_sublayout("minmaxlim","grid"):
            self.params.add_num_edit("minlim",value=self.img_lim[0],limiter=self.img_lim+("coerce",),formatter=("int"),label="Minimal intensity:",add_indicator=True)
            self.params.add_num_edit("maxlim",value=self.img_lim[1],limiter=self.img_lim+("coerce",),formatter=("int"),label="Maximal intensity:",add_indicator=True)
            self.params.add_spacer(width=30,location=(0,2))
        with self.params.using_new_sublayout("presets","hbox"):
            self.params.add_button("save_preset","Save preset")
            self.params.add_button("load_preset","Load preset")
            self.params.vs["save_preset"].connect(self._save_img_lim_preset)
            self.params.vs["load_preset"].connect(self._load_img_lim_preset)
            self.img_lim_preset=self.img_lim
        self.params.add_check_box("show_histogram","Show histogram",value=True).get_value_changed_signal().connect(self._setup_gui_state)
        self.params.add_check_box("auto_histogram_range","Auto histogram range",value=True)
        self.params.add_check_box("show_lines","Show lines",value=True).get_value_changed_signal().connect(self._setup_gui_state)
        with self.params.using_new_sublayout("vline","hbox"):
            self.params.add_spacer(width=20)
            self.params.add_check_box("vlineon","X  ",value=True).get_value_changed_signal().connect(self._setup_gui_state)
            self.params.add_num_edit("vlinepos",value=0,limiter=(0,None,"coerce","float"),formatter=("float","auto",1,True))
        with self.params.using_new_sublayout("hline","hbox"):
            self.params.add_spacer(width=20)
            self.params.add_check_box("hlineon","Y  ",value=True).get_value_changed_signal().connect(self._setup_gui_state)
            self.params.add_num_edit("hlinepos",value=0,limiter=(0,None,"coerce","float"),formatter=("float","auto",1,True))
        self.params.add_button("center_lines","Center lines").get_value_changed_signal().connect(plotter.center_lines)
        self.params.add_check_box("show_linecuts","Show line cuts",value=False).get_value_changed_signal().connect(self._setup_gui_state)
        self.params.add_num_edit("linecut_width",value=1,limiter=(1,None,"coerce","int"),formatter="int",label="Line cut width:")
        self.params.contained_value_changed.connect(lambda n: self.plotter.update_image(update_controls=(n=="normalize"),do_redraw=True),QtCore.Qt.DirectConnection)
        self.params.add_spacer(10)
        self.params.add_toggle_button("update_image","Updating",value=True).get_value_changed_signal().connect(plotter._set_image_update)
        def arm_single():
            self.params.v["update_image"]=False
            self.plotter.arm_single()
        self.params.add_button("single","Single").get_value_changed_signal().connect(arm_single)
        self.params.add_padding()
        def set_img_lim_preset(value):
            self.img_lim_preset=value
        self.add_property_element("img_lim_preset",getter=lambda: self.img_lim_preset,setter=set_img_lim_preset, add_indicator=False)
        def set_colormap(value):
            colormap=dictionary.as_dict(value,style="nested")
            self.plotter.image_window.getHistogramWidget().gradient.restoreState(colormap)
        self.add_property_element("colormap",getter=lambda: self.plotter.image_window.getHistogramWidget().gradient.saveState(),setter=set_colormap,add_indicator=False)  # pylint: disable=unnecessary-lambda
        self._setup_gui_state()

    def set_img_lim(self, *args):
        """
        Set up image value limits.

        Specifies the minimal and maximal values in ``Minimal intensity`` and ``Maximal intensity`` controls.
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
    @controller.exsafeSlot()
    def _save_img_lim_preset(self):
        self.img_lim_preset=self.v["minlim"],self.v["maxlim"]
    @controller.exsafeSlot()
    def _load_img_lim_preset(self):
        self.v["minlim"],self.v["maxlim"]=self.img_lim_preset
    @controller.exsafeSlot()
    def _setup_gui_state(self):
        """Enable or disable controls based on which actions are enabled"""
        self.params.set_enabled("auto_histogram_range",self.v["show_histogram"])
        show_lines=self.v["show_lines"]
        self.params.set_enabled(["vlineon","hlineon","show_linecuts"],show_lines)
        self.params.set_enabled("vlinepos",show_lines and self.v["vlineon"])
        self.params.set_enabled("hlinepos",show_lines and self.v["hlineon"])
        self.params.set_enabled("linecut_width",show_lines and self.v["show_linecuts"])






class ImageItem(pyqtgraph.ImageItem):
    """Minor extension of :class:`pyqtgraph.ImageItem` which keeps track of painting events (last time and number of calls)"""
    def __init__(self, *args, **kwargs):
        pyqtgraph.ImageItem.__init__(self,*args,**kwargs)
        self.paint_cnt=0
        self.paint_time=None
    def paint(self, *args):
        pyqtgraph.ImageItem.paint(self,*args)
        self.paint_time=time.time()
        self.paint_cnt+=1

class PlotCurveItem(pyqtgraph.PlotCurveItem):
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

    class Rectangle:
        def __init__(self, rect, center=None, size=None):
            self.rect=rect
            self.center=center or (0,0)
            self.size=size or (0,0)
        def update_parameters(self, center=None, size=None):
            if center:
                self.center=center
            if size:
                self.size=size
    def setup(self, name=None, img_size=(1024,1024), min_size=None):  # pylint: disable=arguments-differ
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
        self.xbin=1
        self.ybin=1
        self.dec="mean"
        self._updating_image=False
        self._last_paint_time=None
        self._last_img_paint_cnt=None
        self._last_curve_paint_cnt=[None,None]
        if min_size:
            self.setMinimumSize(QtCore.QSize(*min_size))
        self.image_window=pyqtgraph.ImageView(self,imageItem=ImageItem())
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
        self.cut_lines=[PlotCurveItem(pen="#B0B000",name="Horizontal"), PlotCurveItem(pen="#B000B0",name="Vertical")]
        for c in self.cut_lines:
            self.cut_plot_window.addItem(c)
        self.cut_plot_panel.setVisible(False)
        self.set_row_stretch([4,1])
        self.vline.sigPositionChanged.connect(lambda: self.update_image_controls(),QtCore.Qt.DirectConnection)  # pylint: disable=unnecessary-lambda
        self.hline.sigPositionChanged.connect(lambda: self.update_image_controls(),QtCore.Qt.DirectConnection)  # pylint: disable=unnecessary-lambda
        self.vline.sigPositionChanged.connect(lambda: self.lines_updated.emit(),QtCore.Qt.DirectConnection)  # pylint: disable=unnecessary-lambda
        self.hline.sigPositionChanged.connect(lambda: self.lines_updated.emit(),QtCore.Qt.DirectConnection)  # pylint: disable=unnecessary-lambda
        self.image_window.getHistogramWidget().sigLevelsChanged.connect(lambda: self.update_image_controls(levels=self.image_window.getHistogramWidget().getLevels()),QtCore.Qt.DirectConnection)
        self.rectangles={}

    def _attach_controller(self, ctl):
        """
        Attach :class:`ImagePlotterCtl` object.

        Called automatically in :meth:`ImagePlotterCtl.setup`
        """
        self.ctl=ctl
    def _make_virtual_values(self):
        return virtual_gui_values(**{
                "transpose":False,
                "flip_x":False,
                "flip_y":False,
                "normalize":True,
                "show_lines":False,
                "vlineon":False,
                "hlineon":False,
                "show_histogram":True,
                "auto_histogram_range":True,
                "show_linecuts":False,
                "vlinepos":0,
                "hlinepos":0,
                "linecut_width":0,
                "update_image":True})
    def _get_values(self):
        return self.ctl or self._virtual_values
        
    @controller.exsafeSlot(object)
    def _set_image_update(self, do_update):
        self.do_image_update=do_update
    
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
    def set_rectangle(self, name, center=None, size=None):
        """
        Add or change parameters of a rectangle with a given name.

        Rectangle coordinates are specified in the original image coordinate system
        (i.e., rectangles are automatically flipped/transposed/scaled with the image).
        """
        if name not in self.rectangles:
            pqrect=pyqtgraph.ROI((0,0),(0,0),movable=False,pen="#FF00FF")
            self.image_window.getView().addItem(pqrect)
            self.rectangles[name]=self.Rectangle(pqrect)
        rect=self.rectangles[name]
        rect.update_parameters(center,size)
        rcenter=rect.center[0]-rect.size[0]/2.,rect.center[1]-rect.size[1]/2.
        rsize=rect.size
        imshape=self.img.shape
        values=self._get_values()
        rcenter=rcenter[0]/self.xbin,rcenter[1]/self.ybin
        rsize=rsize[0]/self.xbin,rsize[1]/self.ybin
        if values.v["transpose"]:
            rcenter=rcenter[::-1]
            rsize=rsize[::-1]
            imshape=imshape[::-1]
        if values.v["flip_x"]:
            rcenter=(imshape[0]-rcenter[0]-rsize[0]),rcenter[1]
        if values.v["flip_y"]:
            rcenter=rcenter[0],(imshape[1]-rcenter[1]-rsize[1])
        rect.rect.setPos(rcenter)
        rect.rect.setSize(rsize)
    def update_rectangles(self):
        """Update rectangle coordinates"""
        for name in self.rectangles:
            self.set_rectangle(name)
    def del_rectangle(self, name):
        """Delete a rectangle with a given name"""
        if name in self.rectangles:
            rect=self.rectangles.pop(name)
            self.image_window.getView().removeItem(rect)
    def show_rectangles(self, show=True, names=None):
        """
        Toggle showing rectangles on or off
        
        If `names` is given, it specifies names of rectangles to show or hide (by default, all rectangles).
        """
        imgview=self.image_window.getView()
        if names is None:
            names=self.rectangles
        else:
            names=funcargparse.as_sequence(names)
            names=[n for n in names if n in self.rectangles]
        for n in names:
            rect=self.rectangles[n]
            if show and rect.rect not in imgview.addedItems:
                imgview.addItem(rect.rect)
            if (not show) and rect.rect in imgview.addedItems:
                imgview.removeItem(rect.rect)

    lines_updated=Signal()
    @controller.exsafe
    def center_lines(self):
        """Center coordinate lines"""
        imshape=self.img.shape[::-1] if self._get_values().v["transpose"] else self.img.shape
        self.vline.setPos(imshape[0]/2)
        self.hline.setPos(imshape[1]/2)
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
            self.vblines[0].setPos(vpos-cut_width/2)
            self.vblines[1].setPos(vpos+cut_width/2)
            self.hblines[0].setPos(hpos-cut_width/2)
            self.hblines[1].setPos(hpos+cut_width/2)
    def get_line_positions(self):
        """Return lines positions referenced to the original image, taking into account flip/transpose"""
        values=self._get_values()
        if not values.v["show_lines"]:
            return None
        ipos,jpos=values.v["vlinepos"]*self.xbin,values.v["hlinepos"]*self.ybin
        if values.v["flip_x"]:
            ipos=-ipos
        if values.v["flip_y"]:
            jpos=-jpos
        if values.v["transpose"]:
            ipos,jpos=jpos,ipos
        return ipos,jpos
    def set_line_positions(self, ipos=None, jpos=None):
        """Set line positions referenced to the original image, taking into account flip/transpose"""
        values=self._get_values()
        if values.v["transpose"]:
            ipos,jpos=jpos,ipos
        if ipos is not None:
            if values.v["flip_x"]:
                ipos=-ipos  # pylint: disable=invalid-unary-operand-type
            self.vline.setPos(ipos/self.xbin)
        if jpos is not None:
            if values.v["flip_y"]:
                jpos=-jpos  # pylint: disable=invalid-unary-operand-type
            self.hline.setPos(jpos/self.ybin)

    # Update image controls based on PyQtGraph image window
    @controller.exsafeSlot()
    def update_image_controls(self, levels=None):
        """Update image controls in the connected :class:`ImagePlotterCtl` object"""
        if self._updating_image:
            return
        values=self._get_values()
        if levels is not None:
            values.v["minlim"],values.v["maxlim"]=levels
        values.v["vlinepos"]=self.vline.getPos()[0]
        values.v["hlinepos"]=self.hline.getPos()[1]
        self._update_linecut_boundaries(values)
    def _get_min_nonzero(self, img, default=0):
        img=img[img!=0]
        return default if np.all(np.isnan(img)) else np.nanmin(img)
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
        if not self._check_paint_done(dt*0.1):
            return
        with self._while_updating():
            values=self._get_values()
            if not do_redraw:
                if not self.new_image_set and (only_new_image or not self.do_image_update):
                    return
            self.new_image_set=False
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
            img_shape=draw_img.shape
            autoscale=values.v["normalize"]
            all_nan=np.all(np.isnan(draw_img))
            img_levels=[0,1] if all_nan else (np.nanmin(draw_img),np.nanmax(draw_img))
            draw_img=self._sanitize_img(draw_img)
            levels=img_levels if autoscale else (values.v["minlim"],values.v["maxlim"])
            if self.isVisible():
                self.image_window.setImage(draw_img,levels=levels,autoHistogramRange=False)
                if values.v["auto_histogram_range"]:
                    hist_range=min(img_levels[0],levels[0]),max(img_levels[1],levels[1])
                    if hist_range[0]==hist_range[1]:
                        hist_range=hist_range[0]-.5,hist_range[1]+.5
                    self.image_window.ui.histogram.setHistogramRange(*hist_range)
                self._last_img_paint_cnt=self.image_window.imageItem.paint_cnt
            if update_controls:
                with self._while_updating(False):
                    self.update_image_controls(levels=levels if autoscale else None)
            self._show_histogram(values.v["show_histogram"])
            values.i["minlim"]=img_levels[0]
            values.i["maxlim"]=img_levels[1]
            values.v["size"]="{} x {}".format(*img_shape)
            show_lines=values.v["show_lines"]
            vlineon,hlineon=values.v["vlineon"],values.v["hlineon"]
            for ln,lnena in zip([self.vline,self.hline],[vlineon,hlineon]):
                ln.setPen("g" if show_lines and lnena else None)
                ln.setHoverPen("y" if show_lines and lnena else None)
                ln.setMovable(show_lines and lnena)
            for ln in [self.vline]+self.vblines:
                ln.setBounds([0,draw_img.shape[0]])
            for ln in [self.hline]+self.hblines:
                ln.setBounds([0,draw_img.shape[1]])
            self.vline.setPos(values.v["vlinepos"])
            self.hline.setPos(values.v["hlinepos"])
            self._update_linecut_boundaries(values)
            if values.v["show_lines"] and values.v["show_linecuts"]:
                cut_width=values.v["linecut_width"]
                vpos=values.v["vlinepos"]
                vmin=int(min(max(0,vpos-cut_width/2),draw_img.shape[0]-1))
                vmax=int(vpos+cut_width/2)
                if vmax==vmin:
                    if vmin==0:
                        vmax+=1
                    else:
                        vmin-=1
                hpos=values.v["hlinepos"]
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
            self.update_rectangles()
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
    def setup(self, img_size=(1024,1024), min_size=None, ctl_caption=None, name=None, save_values=("colormap","img_lim_preset")):  # pylint: disable=arguments-differ
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