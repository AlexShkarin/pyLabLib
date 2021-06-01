from ..core.thread import controller
from ..core.gui import utils
from ..core.gui.widgets import param_table
from ..core.utils import dictionary
from .widgets.plotters import image_plotter, line_plotter

from ..core.gui import QtWidgets, QtCore



##### Boxes #####

class IBox:
    """
    Generic box controller

    Args:
        box: box widget
        name: box name
    """
    def __init__(self, box, name):
        self.box=box
        self.name=name
        self._deleted=False
    
    def delete(self):
        """Clean up the box widget"""
        self.box.deleteLater()
        self._deleted=True

    def get_all_values(self):
        """Get all GUI values"""
        return {}
    def set_all_values(self, params):
        """Set all GUI values"""
        pass
    def get_all_indicators(self):
        """Get all GUI indicators as a dictionary"""
        return {}


class ParamTableBox(IBox):
    """
    Parameter table box controller

    Args:
        box: box widget
        name: box name
        kwargs: arguments passed to ``setup`` method of the parameters table
    """
    def __init__(self, box, name, **kwargs):
        IBox.__init__(self,box,name)
        self.layout=QtWidgets.QVBoxLayout(box)
        self.layout.setContentsMargins(0,0,0,0)
        self.table=param_table.ParamTable(box)
        kwargs.setdefault("gui_thread_safe",True)
        self.cache_values=kwargs.setdefault("cache_values",True)
        self.table.setup(name=name+"_table",**kwargs)
        self.layout.addWidget(self.table)
        self.v=self.table.v
        self.i=self.table.i

    def __getitem__(self, name):
        return self.table.current_values[name] if self.cache_values else self.table.v[name]
    def __setitem__(self, name, value, force=False):
        return self.table.set_value(name,value,force=force)

    def delete(self):
        self.table.clear(disconnect=True)
        IBox.delete(self)

    def get_all_values(self):
        return self.table.get_all_values()
    def set_all_values(self, params):
        self.table.set_all_values(params)
    def get_all_indicators(self):
        return self.table.get_all_indicators()



class BoxManager:
    """
    Box manager.

    Takes care of creating and cleaning up boxes (containers) in a layout.

    Args:
        frame_widget: base widget (class :class:`.QWidget` or :class:`.QFrame` with a :class:`QBoxLayout` layout) which is the parent widget of the new boxes
        layout: layout into which the boxes are added; by default, `frame_widget` layout
        index_offset: index offset for appending to the new box (by default, put the new boxes to the end; ``index_offset=1`` means that they are added into the next to the last place)
    """
    def __init__(self, frame_widget, layout=None, index_offset=0):
        self.frame_widget=frame_widget
        self.layout=layout or self.frame_widget.layout()
        self.boxes={}
        self.index_offset=index_offset
    
    def _add_box(self, name, caption=None, index=None):
        if caption is not None:
            box=QtWidgets.QGroupBox(self.frame_widget)
            box.setObjectName(name+"_box")
            box.setTitle(caption)
        else:
            box=QtWidgets.QFrame(self.frame_widget)
            box.setObjectName(name+"_box")
        if index is None:
            index=self.layout.count()-self.index_offset
        index=max(0,min(index,self.layout.count()))
        self.layout.insertWidget(index,box)
        return box
    def _add_class_box(self, box_cls, name, caption, index=None, **kwargs):
        if name in self.boxes:
            raise KeyError("box {} already exists".format(name))
        box=self._add_box(name,caption,index=index)
        self.boxes[name]=box_cls(box,name,**kwargs)
        return self.boxes[name]
    @controller.call_in_gui_thread
    def add_empty_box(self, name, caption, index=None):
        """Add an empty box (:class:`IBox`); called synchronously in the GUI thread"""
        return self._add_class_box(IBox,name,caption,index=index)
    @controller.call_in_gui_thread
    def add_param_table_box(self, name, caption, index=None, **kwargs):
        """Add an parameters table box (:class:`ParamTableBox`); called synchronously in the GUI thread"""
        return self._add_class_box(ParamTableBox,name,caption,index=index,**kwargs)
    
    def __getitem__(self, name):
        return self.boxes[name]
    def __contains__(self, name):
        return name in self.boxes
        

    @controller.call_in_gui_thread
    def remove_box(self, name):
        """Delete a box with a given name; called synchronously in the GUI thread"""
        box=self.boxes.pop(name)
        idx=self.layout.indexOf(box.box)
        box.delete()
        utils.delete_layout_item(self.layout,idx)
    @controller.call_in_gui_thread
    def clear(self):
        """Delete all created boxes; called synchronously in the GUI thread"""
        names=list(self.boxes.keys())
        for n in names:
            self.remove_box(n)

    def get_all_values(self):
        """Get all GUI values from all boxes"""
        return dictionary.Dictionary({n:t.get_all_values() for (n,t) in self.boxes.items()})
    def set_all_values(self, params):
        """Set all GUI values for all boxes"""
        for (n,t) in self.boxes.items():
            if n in params:
                t.set_all_values(params[n])
    def get_all_indicators(self):
        """Get all GUI indicators as a dictionary"""
        return dictionary.Dictionary({n:t.get_all_indicators() for (n,t) in self.boxes.items()})







##### Tabs #####

class ITab:
    """
    Generic tab controller

    Args:
        frame: frame widget (class :class:`.QFrame`)
        name: tab name
    """
    def __init__(self, frame, name):
        self.frame=frame
        self.name=name
        self._deleted=False
    
    def delete(self):
        """Clean up the tab frame"""
        self.frame.deleteLater()
        self._deleted=True

    def get_all_values(self):
        """Get all GUI values"""
        return {}
    def set_all_values(self, params):
        """Set all GUI values"""
        pass
    def get_all_indicators(self):
        """Get all GUI indicators as a dictionary"""
        return {}


class BoxTab(ITab):
    """
    Tab controller which contains box manager inside.

    Args:
        frame: frame widget (class :class:`.QFrame`)
        name: tab name
    """
    def __init__(self, frame, name):
        ITab.__init__(self,frame,name)
        self.layout=QtWidgets.QVBoxLayout(frame)
        spacer=QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(spacer)
        self.layout.setStretch(0,1)
        self.boxes=BoxManager(frame,index_offset=1)

    def get_all_values(self):
        return self.boxes.get_all_values()
    def set_all_values(self, params):
        self.boxes.set_all_values(params)
    def get_all_indicators(self):
        return self.boxes.get_all_indicators()


class IAutoupdateTab(ITab):
    """
    Auto-updateable tab.

    Can be set up to be updated periodically in the GUI thread.

    Args:
        frame: frame widget (class :class:`.QFrame`)
        name: tab name
        update_func: if not ``None``, specifies external update function
    """
    def __init__(self, frame, name, update_func=None):
        ITab.__init__(self,frame,name)
        self.timer=QtCore.QTimer(frame)
        self.timer.timeout.connect(self._autoupdate)
        self._update_func=update_func
    
    def _update(self): # to be overloaded
        if self._update_func is not None:
            self._update_func()
    
    @controller.exsafe
    def _autoupdate(self):
        if not self._deleted:
            self._update()
    @controller.call_in_gui_thread
    def update(self):
        """Explicitly update the tab (called synchronously in the GUI thread)"""
        self._update()
    @controller.call_in_gui_thread
    def setup_autoupdate(self, period=None):
        """
        Setup autoupdate period.

        If `period` is ``None``, turn the autoupdate off.
        """
        if period is None or period<=0:
            self.timer.stop()
        else:
            self.timer.start(period*1000)
    
    def delete(self):
        self.timer.stop()
        ITab.delete(self)


class ImageTab(IAutoupdateTab):
    """
    Image plotter tab.

    The tab which contains :class:`.ImageView` and :class:`.ImagePlotterCtl` widgets to show images.
    The image can be changed in a thread-safe manner, and updated automatically or explicitly.
    """
    def __init__(self, frame, name):
        IAutoupdateTab.__init__(self,frame,name)
        self.layout=QtWidgets.QHBoxLayout(frame)
        self.layout.setContentsMargins(0,0,0,0)
        self.imview=image_plotter.ImagePlotter(frame)
        self.imview.setup(name=name+"_image_view",img_size=(1,1))
        self.layout.addWidget(self.imview)
        self.imctl=image_plotter.ImagePlotterCtl(frame)
        self.imctl.setup(name=name+"_image_view_ctl",plotter=self.imview)
        self.imctl.setMinimumSize(200,0)
        self.imctl.setMaximumSize(200,2**16)
        self.side_layout=QtWidgets.QVBoxLayout()
        self.side_layout.addWidget(self.imctl)
        self.layout.addLayout(self.side_layout)
        self.imctl.set_img_lim(None,None)
        self.imctl.set_all_values({"update_image":True})
        self.box_manager=BoxManager(self,layout=self.side_layout)

    def set_image(self, img, update=False):
        """
        Set a new image to display.

        The method is thread-safe, but the displayed image only changes on the update (either explicit, or autoupdate).
        If ``update==True``, update after setting the image.
        """
        self.imview.set_image(img)
        if update:
            self.update()
    
    def _update(self):
        self.imview.update_image(update_controls=True)

    def get_all_values(self):
        return self.imctl.get_all_values()
    def set_all_values(self, params):
        self.imctl.set_all_values(params)
    def get_all_indicators(self):
        return self.imctl.get_all_indicators()



class LinePlotTab(IAutoupdateTab):
    """
    Line plotter tab.

    The tab which contains a :class:`.LinePlotter` widget to show line plots.
    The plot traces can be changed in a thread-safe manner, and updated automatically or explicitly.
    """
    def __init__(self, frame, name):
        IAutoupdateTab.__init__(self,frame,name)
        self.layout=QtWidgets.QHBoxLayout(frame)
        self.layout.setContentsMargins(0,0,0,0)
        self.plotter=line_plotter.LinePlotter(frame)
        self.layout.addWidget(self.plotter)
        
    def set_traces(self, data):
        """
        Set a new trace data to display.

        The method is thread-safe, but the displayed traces only changes on the update (either explicit, or autoupdate)
        """
        self.plotter.set_traces(data)

    def _update(self):
        self.plotter.update_traces()





class TabManager:
    """
    Tab manager.

    Takes care of creating and cleaning up tabs.

    Args:
        tab_widget: base tab widget (class :class:`.QTabWidget`) into which the tabs are added.
    """
    def __init__(self, tab_widget):
        self.tab_widget=tab_widget
        self.tabs={}
    
    def _add_tab_frame(self, caption, index=None):
        tab=QtWidgets.QFrame(self.tab_widget)
        if index is None:
            index=self.tab_widget.count()
        index=max(0,min(index,self.tab_widget.count()))
        self.tab_widget.insertTab(index,tab,caption)
        return tab
    def _add_class_tab_frame(self, tab_cls, name, caption, *args, index=None):
        if name in self.tabs:
            raise KeyError("tab {} already exists".format(name))
        tab=self._add_tab_frame(caption,index=index)
        self.tabs[name]=tab_cls(tab,name,*args)
        return self.tabs[name]
    @controller.call_in_gui_thread
    def add_empty_tab(self, name, caption, update_func=None, index=None):
        """
        Add an empty tab (:class:`ITab` or :class:`IAutoupdateTab`); called synchronously in the GUI thread
        
        If `update_func` is not ``None``, it can specify a function for tab update and autoupdate, which will be called in the GUI thread
        (either on explicit request, or periodically).
        """
        if update_func is None:
            return self._add_class_tab_frame(ITab,name,caption,index=index)
        else:
            return self._add_class_tab_frame(IAutoupdateTab,name,caption,update_func,index=index)
    @controller.call_in_gui_thread
    def add_image_tab(self, name, caption, index=None):
        """Add an image tab (:class:`ImageTab`); called synchronously in the GUI thread"""
        return self._add_class_tab_frame(ImageTab,name,caption,index=index)
    @controller.call_in_gui_thread
    def add_line_plot_tab(self, name, caption, index=None):
        """Add an line plot tab (:class:`LinePlotTab`); called synchronously in the GUI thread"""
        return self._add_class_tab_frame(LinePlotTab,name,caption,index=index)
    @controller.call_in_gui_thread
    def add_box_tab(self, name, caption, index=None):
        """Add an box tab (:class:`BoxTab`); called synchronously in the GUI thread"""
        return self._add_class_tab_frame(BoxTab,name,caption,index=index)

    def __getitem__(self, name):
        return self.tabs[name]
    def __contains__(self, name):
        return name in self.tabs
        

    @controller.call_in_gui_thread
    def remove_tab(self, name):
        """Delete a tab with a given name; called synchronously in the GUI thread"""
        tab=self.tabs.pop(name)
        idx=self.tab_widget.indexOf(tab.frame)
        self.tab_widget.removeTab(idx)
        tab.delete()
    @controller.call_in_gui_thread
    def clear(self):
        """Delete all created tabs; called synchronously in the GUI thread"""
        names=list(self.tabs.keys())
        for n in names:
            self.remove_tab(n)

    def get_all_values(self):
        """Get all GUI values from all tabs"""
        return dictionary.Dictionary({n:t.get_all_values() for (n,t) in self.tabs.items()})
    def set_all_values(self, params):
        """Set all GUI values for all tabs"""
        for (n,t) in self.tabs.items():
            if n in params:
                t.set_all_values(params[n])
    def get_all_indicators(self):
        """Get all GUI indicators as a dictionary"""
        return dictionary.Dictionary({n:t.get_all_indicators() for (n,t) in self.tabs.items()})