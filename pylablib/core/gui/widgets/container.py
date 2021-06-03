from ...utils import general, dictionary
from .. import value_handling
from .. import QtCore, QtWidgets
from ...thread import controller
from .layout_manager import QLayoutManagedWidget

import collections




TTimer=collections.namedtuple("TTimer",["name","period","timer"])
TTimerEvent=collections.namedtuple("TTimerEvent",["start","loop","stop","timer"])
TChild=collections.namedtuple("TChild",["name","widget","gui_values_path"])
class QContainer(QtCore.QObject):
    """
    Basic controller object which combines and controls several other widget.

    Can either corresponds to a widget (e.g., a frame or a group box), or simply be an organizing entity.

    Args:
        name: entity name (used by default when adding this object to a values table)
    """
    TimerUIDGenerator=general.NamedUIDGenerator(thread_safe=True)
    def __init__(self, *args, name=None, **kwargs):
        super().__init__(*args,**kwargs)
        self.name=None
        self.setup_name(name)
        self._timers={}
        self._timer_events={}
        self._running=False
        self._children=dictionary.Dictionary()
        self.setup_gui_values("new")
        self.ctl=None
        self.w=dictionary.ItemAccessor(self.get_widget)
        self.c=dictionary.ItemAccessor(self.get_child)
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)
        self.i=dictionary.ItemAccessor(self.get_indicator,self.set_indicator)

    _ignore_set_values=[]
    _ignore_get_values=[]
    def setup_gui_values(self, gui_values="new", gui_values_path=""):
        """
        Setup container's GUI values storage.

        `gui_values` is a :class:`.GUIValues`` object, an object which has ``gui_values`` attribute,
        or ``"new"`` (make a new storage; in this case `gui_values_path` is ignored), and
        `gui_values_path` is the container's path within this storage.
        """
        if self._children:
            raise RuntimeError("can not change gui values after children have been added")
        if gui_values is not None:
            self.gui_values,self.gui_values_path=value_handling.get_gui_values(gui_values,gui_values_path)
    def setup_name(self, name):
        """Set the object's name"""
        if name is not None:
            self.name=name
            self.setObjectName(name)
    def setup(self, name=None, gui_values=None, gui_values_path=""):
        """
        Setup the container by initializing its GUI values and setting the ``ctl`` attribute.

        `gui_values` is a :class:`.GUIValues`` object, an object which has ``gui_values`` attribute,
        or ``"new"`` (make a new storage; in this case `gui_values_path` is ignored), and
        `gui_values_path` is the container's path within this storage.
        If ``gui_values`` is ``None``, skip the setup (assume that it's already done).
        """
        if self.name is None:
            self.setup_name(name)
        self.setup_gui_values(gui_values=gui_values,gui_values_path=gui_values_path)
        self.ctl=controller.get_gui_controller()

    def add_timer(self, name, period, autostart=True):
        """
        Add a periodic timer with the given `name` and `period`.

        Rarely needs to be called explicitly (one is created automatically if timer event is created).
        If ``autostart==True`` and the container has been started (by calling :meth:`start` method), start the timer as well.
        """
        if name is None:
            while True:
                name=self.TimerUIDGenerator("timer")
                if name not in self._timers:
                    break
        if name in self._timers:
            raise ValueError("timer {} already exists".format(name))
        timer=QtCore.QTimer(self)
        timer.timeout.connect(controller.exsafe(lambda : self._on_timer(name)))
        self._timers[name]=TTimer(name,period,timer)
        if self._running and autostart:
            self.start_timer(name)
        return name
    def _get_timer(self, name):
        if name not in self._timers:
            raise KeyError("timer {} does not exist".format(name))
        return self._timers[name]
    def start_timer(self, name):
        """Start the timer with the given name (also called automatically on :meth:`start` method)"""
        if not self.is_timer_running(name):
            self._call_timer_events(name,"start")
        _,period,timer=self._get_timer(name)
        timer.start(max(int(period*1000),1))
    def stop_timer(self, name):
        """Stop the timer with the given name (also called automatically on :meth:`stop` method)"""
        running=self.is_timer_running(name)
        _,_,timer=self._get_timer(name)
        if running:
            timer.stop()
            self._call_timer_events(name,"stop")
    def is_timer_running(self, name):
        """Check if the timer with the given name is running"""
        _,_,timer=self._get_timer(name)
        return timer.isActive()
    def _on_timer(self, name):
        self._call_timer_events(name,"loop")
    
    def add_timer_event(self, name, loop=None, start=None, stop=None, period=None, timer=None, autostart=True):
        """
        Add timer event with the given `name`.

        Add an event which should be called periodically (e.g., a GUI update). Internally implemented through Qt timers.
        `loop`, `start` and `stop` are the functions called, correspondingly, on timer (periodically), when timer is start, and when it's finished.
        One can either specify the timer by name (`timer` parameter), or create a new one with the given `period`.
        If ``autostart==True`` and the container has been started (by calling :meth:`start` method), start the timer as well.
        """
        if timer is None and period is None:
            raise ValueError("either a period or a timer name should be provided")
        if timer is None:
            timer=self.add_timer(None,period,autostart=autostart)
        if start is not None and self.is_timer_running(timer):
            start()
        self._timer_events[name]=TTimerEvent(start,loop,stop,timer)
        return timer
    def _call_timer_events(self, timer, meth="loop"):
        t=self._get_timer(timer).timer
        for evt in self._timer_events.values():
            if evt.timer==timer:
                if meth=="start" and evt.start is not None:
                    evt.start()
                elif meth=="stop" and evt.stop is not None:
                    evt.stop()
                elif evt.loop is not None and t.isActive(): # discard all possible after-stop queued events
                    evt.loop()

    def add_child_values(self, path, widget):
        """
        Add child's values to the container's table.

        If `widget` is a container and ``path==""`` or ends in ``"/*"`` (e.g., ``"subpath/*"``),
        use its :meth:`setup_gui_values` to make it share the same GUI values;
        otherwise, simply add it to the GUI values under the given path.
        """
        if path=="" or path=="*" or path.endswith("/*"):
            if path.endswith("*"):
                path=path[:-1]
            if hasattr(widget,"setup_gui_values"):
                widget.setup_gui_values(self,path)
            else:
                raise ValueError("can not store a non-container widget under an empty path")
        else:
            self.gui_values.add_widget(path,widget)
    def _setup_child_name(self, widget, name):
        if name is None:
            name=getattr(widget,"name",None)
            if name is None:
                raise ValueError("widget name must be provided")
        elif hasattr(widget,"setup_name"):
            widget.setup_name(name)
        return name
    def add_child(self, name, widget, gui_values_path=True):
        """
        Add a contained child widget.

        If `gui_values_path` is ``False`` or ``None``, do not add it to the GUI values table;
        if it is ``True``, add it under the same root (``path==""``) if it's a container, and under `name` if it's not;
        otherwise, ``gui_values_path`` specifies the path under which the widget values are stored.
        """
        name=self._setup_child_name(widget,name)
        if name in self._children:
            raise ValueError("child {} is already present")
        if gui_values_path!=False and gui_values_path is not None:
            if gui_values_path==True:
                gui_values_path="" if hasattr(widget,"setup_gui_values") else name
            self.add_child_values(gui_values_path,widget)
        self._children[name]=TChild(name,widget,gui_values_path)
        return widget
    def get_child(self, name):
        """Get the child widget with the given name"""
        path,subpath=self._children.get_max_prefix(name,kind="leaf")
        if path:
            return self._children[path].widget.get_child(subpath) if subpath else self._children[path].widget
        raise KeyError("can't find widget {}".format(name))
    def _clear_child(self, child):
        if hasattr(child.widget,"clear"):
            child.widget.clear()
        if child.gui_values_path is not None:
            try:
                self.gui_values.remove_handler((self.gui_values_path,child.gui_values_path),remove_indicator=True,disconnect=True)
            except KeyError:
                pass
    def remove_child(self, name):
        """Remove child from the container and clear it"""
        path,subpath=self._children.get_max_prefix(name,kind="leaf")
        if path:
            if subpath:
                return self._children[path].widget.remove_child(subpath)
            ch=self._children.pop(path)
            self._clear_child(ch)
        else:
            raise KeyError("can't find widget {}".format(name))

    @controller.exsafe
    def start(self):
        """
        Start the container.

        Starts all the internal timers, and calls ``start`` method for all the contained widgets.
        """
        if self._running:
            raise RuntimeError("container '{}' loop is already running".format(self.name))
        for ch in self._children.iternodes():
            if hasattr(ch.widget,"start"):
                ch.widget.start()
        for n in self._timers:
            self.start_timer(n)
        self._running=True
    @controller.exsafe
    def stop(self):
        """
        Stop the container.

        Stops all the internal timers, and calls ``stop`` method for all the contained widgets.
        """
        if not self._running:
            raise RuntimeError("container '{}' loop is not running".format(self.name))
        self._running=False
        for n in self._timers:
            self.stop_timer(n)
        for ch in self._children.iternodes():
            if hasattr(ch.widget,"stop"):
                ch.widget.stop()

    def clear(self):
        """
        Clear the container.

        Stop all timers and widgets, and call ``clear`` methods of all contained widgets,
        remove all widgets from the values table, remove all widgets from the table.
        """
        if self._running:
            self.stop()
        for ch in self._children.iternodes():
            self._clear_child(ch)
        self._children=dictionary.Dictionary()

    def get_handler(self, name):
        """Get value handler of a widget with the given name"""
        return self.gui_values.get_handler((self.gui_values_path,name or ""))
    def get_widget(self, name):
        return self.gui_values.get_widget((self.gui_values_path,name or ""))
    def get_value(self, name=None):
        """Get value of a widget with the given name (``None`` means all values)"""
        return self.gui_values.get_value((self.gui_values_path,name or ""))
    def get_all_values(self):
        """Get values of all widget in the container"""
        return self.gui_values.get_all_values(self.gui_values_path,exclude=self._ignore_get_values)
    def set_value(self, name, value):
        """Set value of a widget with the given name (``None`` means all values)"""
        return self.gui_values.set_value((self.gui_values_path,name or ""),value)
    def set_all_values(self, values):
        """Set values of all widgets in the container"""
        return self.gui_values.set_all_values(values,self.gui_values_path,exclude=self._ignore_set_values)

    def get_indicator(self, name=None):
        """Get indicator value for a widget with the given name (``None`` means all indicators)"""
        return self.gui_values.get_indicator((self.gui_values_path,name or ""))
    def get_all_indicators(self):
        """Get indicator values of all widget in the container"""
        return self.gui_values.get_all_indicators(self.gui_values_path)
    def set_indicator(self, name, value, ignore_missing=True):
        """Set indicator value for a widget or a branch with the given name"""
        return self.gui_values.set_indicator((self.gui_values_path,name or ""),value,ignore_missing=ignore_missing)
    set_all_indicators=set_indicator
    def update_indicators(self):
        """Update all indicators to represent current values"""
        return self.gui_values.update_indicators(root=self.gui_values_path)





class QWidgetContainer(QLayoutManagedWidget, QContainer):
    """
    Generic widget container.

    Combines :class:`QContainer` management of GUI values and timers
    with :class:`.QLayoutManagedWidget` management of the contained widget's layout.

    Typically, adding widget adds them both to the container values and to the layout;
    however, this can be skipped by either using :meth:`.QLayoutManagedWidget.add_to_layout`
    (only add to the layout), or specifying ``location="skip"`` in :meth:`add_child` (only add to the container).
    """
    def setup(self, layout="vbox", no_margins=False, name=None, gui_values=None, gui_values_path=""):
        QContainer.setup(self,name=name,gui_values=gui_values,gui_values_path=gui_values_path)
        QLayoutManagedWidget.setup(self,layout=layout,no_margins=no_margins)
    def add_child(self, name, widget, location=None, gui_values_path=True):
        """
        Add a contained child widget.

        `name` specifies the child storage name;
        if ``name==False``, only add the widget to they layout, but not to the container.
        `location` specifies the layout location to which the widget is added;
        if ``location=="skip"``, skip adding it to the layout (can be manually added later).
        Note that if the widget is added to the layout, it will be completely deleted
        when :meth:`clear`or :meth:`remove_child` methods are called;
        otherwise, simply its ``clear`` method will be called, and its GUI values will be deleted.

        If `gui_values_path` is ``False`` or ``None``, do not add it to the GUI values table;
        if it is ``True``, add it under the same root (``path==""``) if it's a container, and under `name` if it's not;
        otherwise, ``gui_values_path`` specifies the path under which the widget values are stored.
        """
        if name!=False:
            QContainer.add_child(self,name=name,widget=widget,gui_values_path=gui_values_path)
        if isinstance(widget,QtWidgets.QWidget):
            QLayoutManagedWidget.add_to_layout(self,widget,location=location)
        return widget
    def remove_child(self, name):
        """Remove widget from the container and the layout, clear it, and remove it"""
        if name in self._children:
            widget=self._children[name].widget
            QContainer.remove_child(self,name)
            QLayoutManagedWidget.remove_layout_element(self,widget)
        else:
            QContainer.remove_child(self,name)
    def add_frame(self, name, layout="vbox", location=None, gui_values_path=True, no_margins=True):
        """
        Add a new frame container to the layout.

        `layout` specifies the layout (``"vbox"``, ``"hbox"``, or ``"grid"``) of the new frame,
        and `location` specifies its location within the container layout.
        If ``no_margins==True``, the frame will have no inner layout margins.
        The other parameters are the same as in :meth:`add_child` method.
        """
        frame=QFrameContainer(self)
        self.add_child(name,frame,location=location,gui_values_path=gui_values_path)
        frame.setup(layout=layout,no_margins=no_margins)
        return frame
    def add_group_box(self, name, caption, layout="vbox", location=None, gui_values_path=True, no_margins=True):
        """
        Add a new group box container with the given `caption` to the layout.

        `layout` specifies the layout (``"vbox"``, ``"hbox"``, or ``"grid"``) of the new frame,
        and `location` specifies its location within the container layout.
        If ``no_margins==True``, the frame will have no inner layout margins.
        The other parameters are the same as in :meth:`add_child` method.
        """
        group_box=QGroupBoxContainer(self)
        self.add_child(name,group_box,location=location,gui_values_path=gui_values_path)
        group_box.setup(caption=caption,layout=layout,no_margins=no_margins)
        return group_box
    def clear(self):
        """
        Clear the container.

        All the timers are stopped, all the contained widgets are cleared and removed.
        """
        QContainer.clear(self)
        QLayoutManagedWidget.clear(self)




class QFrameContainer(QtWidgets.QFrame, QWidgetContainer):
    """An extension of :class:`QWidgetContainer` for a ``QFrame`` Qt base class"""

class QGroupBoxContainer(QtWidgets.QGroupBox, QWidgetContainer):
    """An extension of :class:`QWidgetContainer` for a ``QGroupBox`` Qt base class"""
    def setup(self, caption=None, layout="vbox", no_margins=False, name=None, gui_values=None, gui_values_path=""):
        QWidgetContainer.setup(self,layout=layout,no_margins=no_margins,name=name,gui_values=gui_values,gui_values_path=gui_values_path)
        if caption is not None:
            self.setTitle(caption)




class QTabContainer(QtWidgets.QTabWidget, QContainer):
    """
    Container which manages tab widget.

    Does not have its own layout, but can add or remove tabs, which are represented as :class:`QFrameContainer` widgets.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self._tabs={}
    def add_tab(self, name, caption, index=None, layout="vbox", gui_values_path=True, no_margins=True):
        """
        Add a new tab container with the given `caption` to the widget.

        `index` specifies the new tab's index (``None`` means adding to the end, negative values count from the end).
        `layout` specifies the layout (``"vbox"``, ``"hbox"``, or ``"grid"``) of the new frame,
        and `location` specifies its location within the container layout.
        If ``no_margins==True``, the frame will have no inner layout margins.
        The other parameters are the same as in :meth:`add_child` method.
        """
        if name in self._tabs:
            raise ValueError("tab {} already exists".format(name))
        frame=QFrameContainer(self)
        self.add_child(name=name,widget=frame,gui_values_path=gui_values_path)
        frame.setup(layout=layout,no_margins=no_margins)
        if index is None:
            index=self.count()
        elif index<0:
            index=index%self.count()
        else:
            index=min(index,self.count())
        self.insertTab(index,frame,caption)
        self._tabs[name]=frame
        return frame
    def remove_tab(self, name):
        """
        Remove a tab with the given name.

        Clear it, remove its GUI values, and delete it and all contained widgets.
        """
        super().remove_child(name)
        frame=self._tabs.pop(name)
        idx=self.indexOf(frame)
        self.removeTab(idx)
        frame.deleteLater()
    def clear(self):
        for n in list(self._tabs):
            self.remove_tab(n)
        super().clear()