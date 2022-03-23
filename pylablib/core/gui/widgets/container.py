from ...utils import general, dictionary
from .. import value_handling
from ..value_handling import _hasattr
from .. import QtCore, QtWidgets, Signal
from ...thread import controller
from .layout_manager import IQLayoutManagedWidget

import collections




TTimer=collections.namedtuple("TTimer",["name","period","timer"])
TTimerEvent=collections.namedtuple("TTimerEvent",["start","loop","stop","timer"])
TChild=collections.namedtuple("TChild",["name","widget","gui_values_path"])
class IQContainer:
    """
    Basic controller object which combines and controls several other widget.

    Can either corresponds to a widget (e.g., a frame or a group box), or simply be an organizing entity.

    Args:
        name: entity name (used by default when adding this object to a values table)
    
    Abstract mix-in class, which needs to be added to a class inheriting from ``QObject``.
    Alternatively, one can directly use :class:`QContainer`, which already inherits from ``QObject``.
    """
    TimerUIDGenerator=general.NamedUIDGenerator(thread_safe=True)
    def __init__(self, *args, name=None, **kwargs):
        if not isinstance(self,QtCore.QObject):
            raise RuntimeError("IQContainer should be mixed with a QObject class or subclass")
        super().__init__(*args,**kwargs)
        self.name=None
        self.setup_name(name)
        self._timers={}
        self._timer_events={}
        self._running=False
        self._stopping=False
        self._children=dictionary.Dictionary()
        self.gui_values=value_handling.GUIValues()
        self.ctl=None
        self.c=dictionary.ItemAccessor(self.get_child)
        self.w=dictionary.ItemAccessor(self.get_widget)
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)
        self.i=dictionary.ItemAccessor(self.get_indicator,self.set_indicator)

    _ignore_set_values=[]
    _ignore_get_values=[]
    contained_value_changed=Signal(object,object)
    def setup_name(self, name):
        """Set the object's name"""
        if name is not None:
            self.name=name
            self.setObjectName(name)  # pylint: disable=no-member
    def setup(self, name=None):
        """Setup the container by initializing its GUI values and setting the ``ctl`` attribute"""
        if self.name is None:
            self.setup_name(name)
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
        timer.timeout.connect(controller.exsafe(lambda: self._on_timer(name)))
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
        if name in self._timer_events:
            raise ValueError("timer event {} already exists".format(name))
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

    def add_child_values(self, name, widget, path, add_change_event=True):
        """
        Add child's values to the container's table.

        If `widget` is a container and ``path==""`` or ends in ``"/*"`` (e.g., ``"subpath/*"``),
        use its ``setup_gui_values`` to make it share the same GUI values;
        otherwise, simply add it to the GUI values under the given path.
        if ``add_change_event==True``, changing of the widget's value emits the container's ``contained_value_changed`` event
        """
        path=self._normalize_name(path)
        if path=="" or path=="*" or path.endswith("/*"):
            if path.endswith("*"):
                path=path[:-1]
            self.gui_values.add_widget((path,"."+name),widget)
        else:
            self.gui_values.add_widget(path,widget)
        if add_change_event:
            if _hasattr(widget,"value_changed"):
                widget.value_changed.connect(lambda value: self.contained_value_changed.emit(path,value))
            elif _hasattr(widget,"contained_value_changed"):
                widget.contained_value_changed.connect(lambda name,value: self.contained_value_changed.emit(self._normalize_name((path,name)),value))
    def _setup_child_name(self, widget, name):
        if name is None:
            name=getattr(widget,"name",None)
            if name is None:
                raise ValueError("widget name must be provided")
        elif _hasattr(widget,"setup_name"):
            widget.setup_name(name)
        return name
    def add_child(self, name, widget, gui_values_path=True, add_change_event=True):
        """
        Add a contained child widget.

        If `gui_values_path` is ``False`` or ``None``, do not add it to the GUI values table;
        if it is ``True``, add it under the same root (``path==""``) if it's a container, and under `name` if it's not;
        otherwise, ``gui_values_path`` specifies the path under which the widget values are stored.
        if ``add_change_event==True``, changing of the widget's value emits the container's ``contained_value_changed`` event
        """
        name=self._setup_child_name(widget,name)
        if name in self._children:
            raise ValueError("child {} is already present".format(name))
        if gui_values_path!=False and gui_values_path is not None:
            if gui_values_path==True:
                gui_values_path="" if _hasattr(widget,"get_all_values") else name
            self.add_child_values(name,widget,gui_values_path,add_change_event=add_change_event)
        else:
            gui_values_path=None
        self._children[name]=TChild(name,widget,gui_values_path)
        return widget
    def get_child(self, name):
        """Get the child widget with the given name"""
        path,subpath=self._children.get_max_prefix(name,kind="leaf")
        if path:
            return self._children[path].widget.get_child(subpath) if subpath else self._children[path].widget
        raise KeyError("can't find widget {}".format(name))
    def _clear_child(self, child):
        if _hasattr(child.widget,"clear"):
            child.widget.clear()
        if child.gui_values_path is not None:
            try:
                self.gui_values.remove_handler(child.gui_values_path,remove_indicator=True,disconnect=True)
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
    def add_virtual_element(self, name, value=None, multivalued=False, add_indicator=True):
        """
        Add a virtual value element.

        Doesn't correspond to any actual widget, but behaves very similarly from the application point of view
        (its value can be set or read, it has on-change events, it can have indicator).
        The element value is simply stored on set and retrieved on get.
        If ``multivalued==True``, the internal value is assumed to be complex, so it is forced to be a :class:`.Dictionary` every time it is set.
        If ``add_indicator==True``, add default indicator handler as well.
        """
        self.gui_values.add_virtual_element(name,value=value,multivalued=multivalued,add_indicator=add_indicator)
    def add_property_element(self, name, getter=None, setter=None, add_indicator=True):
        """
        Add a property value element.

        Doesn't correspond to any actual widget, but behaves very similarly from the application point of view;
        each time the value is set or get, the corresponding setter and getter methods are called.
        If ``add_indicator==True``, add default (stored value) indicator handler as well.
        """
        self.gui_values.add_property_element(name,getter=getter,setter=setter,add_indicator=add_indicator)

    @controller.exsafe
    def start(self):
        """
        Start the container.

        Starts all the internal timers, and calls ``start`` method for all the contained widgets.
        """
        if self._running:
            return
        for ch in self._children.iternodes():
            if _hasattr(ch.widget,"start"):
                ch.widget.start()
        for n in self._timers:
            self.start_timer(n)
        self._stopping=False
        self._running=True
    def _notify_stop(self):
        if not self._stopping:
            self._stopping=True
            for ch in self._children.iternodes():
                if _hasattr(ch.widget,"_notify_stop"):
                    ch.widget._notify_stop()
    @controller.exsafe
    def stop(self):
        """
        Stop the container.

        Stops all the internal timers, and calls ``stop`` method for all the contained widgets.
        """
        if not self._running:
            return
        self._notify_stop()
        self._running=False
        for n in self._timers:
            self.stop_timer(n)
        for ch in self._children.iternodes():
            if _hasattr(ch.widget,"stop"):
                ch.widget.stop()
    def is_running(self):
        """Check if the container is running (started and not yet stopped)"""
        return self._running
    def is_stopping(self):
        """Check if the container is stopping (stopping initialized and not yet done)"""
        return self._stopping

    def clear(self):
        """
        Clear the container.

        Stop all timers and widgets, and call ``clear`` methods of all contained widgets,
        remove all widgets from the values table, remove all widgets from the table.
        """
        if self._running:
            self.stop()
        for ch in self._children.paths():
            self.remove_child(ch)
        self._children=dictionary.Dictionary()


    def _filter_values(self, values, exclude):
        if exclude and any(k in values for k in exclude):
            values=values.copy()
            for v in exclude:
                if v in values:
                    del values[v]
        return values
    def _normalize_name(self, name):
        if isinstance(name,tuple):
            name=dictionary.normalize_path(name)
        if isinstance(name,(list,tuple)):
            return "/".join(name)
        return name
    def get_handler(self, name):
        """Get value handler of a widget with the given name"""
        return self.gui_values.get_handler(name)
    def get_widget(self, name):
        """Get a widget corresponding to a value with the given name"""
        return self.gui_values.get_widget(name)

    def get_value(self, name=None):
        """Get value of a widget with the given name (``None`` means all values)"""
        return self.gui_values.get_value(name)
    def get_all_values(self):
        """Get values of all widget in the container"""
        return self._filter_values(self.gui_values.get_all_values(),self._ignore_get_values)
    def set_value(self, name, value):
        """Set value of a widget with the given name (``None`` means all values)"""
        return self.gui_values.set_value(name,value)
    def set_all_values(self, value):
        """Set values of all widgets in the container"""
        return self.gui_values.set_all_values(self._filter_values(value,self._ignore_set_values))
    def get_value_changed_signal(self, name):
        """Get a value-changed signal for a widget with the given name"""
        return self.gui_values.get_value_changed_signal(name)
    def update_value(self, name=None):
        """
        Send update signal for a handler with a given name or list of names.
        
        Emit a value changed signal with the current value to notify the subscribed slots.
        If `name` is ``None``, emit for all values in the table.
        """
        return self.gui_values.update_value(name=name)

    def get_indicator(self, name=None):
        """Get indicator value for a widget with the given name (``None`` means all indicators)"""
        return self.gui_values.get_indicator(name)
    def get_all_indicators(self):
        """Get indicator values of all widget in the container"""
        return self.gui_values.get_all_indicators()
    def set_indicator(self, name, value, ignore_missing=False):
        """Set indicator value for a widget or a branch with the given name"""
        return self.gui_values.set_indicator(name,value,ignore_missing=ignore_missing)
    def set_all_indicators(self, value, ignore_missing=True):
        return self.gui_values.set_all_indicators(value,ignore_missing=ignore_missing)
    def update_indicators(self):
        """Update all indicators to represent current values"""
        return self.gui_values.update_indicators()


class QContainer(IQContainer, QtCore.QObject):
    """
    Basic controller object which combines and controls several other widget.

    Can either corresponds to a widget (e.g., a frame or a group box), or simply be an organizing entity.

    Args:
        name: entity name (used by default when adding this object to a values table)
    
    Simply a combination of :class:`IQContainer` and ``QObject``.
    """




class IQWidgetContainer(IQLayoutManagedWidget, IQContainer):
    """
    Generic widget container.

    Combines :class:`IQContainer` management of GUI values and timers
    with :class:`.IQLayoutManagedWidget` management of the contained widget's layout.

    Typically, adding widget adds them both to the container values and to the layout;
    however, this can be skipped by either using :meth:`.QLayoutManagedWidget.add_to_layout`
    (only add to the layout), or specifying ``location="skip"`` in :meth:`add_child` (only add to the container).
    
    Abstract mix-in class, which needs to be added to a class inheriting from ``QWidget``.
    Alternatively, one can directly use :class:`QWidgetContainer`, which already inherits from ``QWidget``.
    """
    def setup(self, layout="vbox", no_margins=False, name=None):  # pylint: disable=arguments-differ, arguments-renamed
        IQContainer.setup(self,name=name)
        IQLayoutManagedWidget.setup(self,layout=layout,no_margins=no_margins)
    def add_child(self, name, widget, location=None, gui_values_path=True):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Add a contained child widget.

        `name` specifies the child storage name;
        if ``name==False``, only add the widget to they layout, but not to the container.
        `location` specifies the layout location to which the widget is added;
        if ``location=="skip"``, skip adding it to the layout (can be manually added later).
        Note that if the widget is added to the layout, it will be completely deleted
        when ``clear`` or ``remove_child`` methods are called;
        otherwise, simply its ``clear`` method will be called, and its GUI values will be deleted.

        If `gui_values_path` is ``False`` or ``None``, do not add it to the GUI values table;
        if it is ``True``, add it under the same root (``path==""``) if it's a container, and under `name` if it's not;
        otherwise, ``gui_values_path`` specifies the path under which the widget values are stored.
        """
        if name!=False:
            IQContainer.add_child(self,name=name,widget=widget,gui_values_path=gui_values_path)
        if isinstance(widget,QtWidgets.QWidget):
            IQLayoutManagedWidget.add_to_layout(self,widget,location=location)
        return widget
    def remove_child(self, name):
        """Remove widget from the container and the layout, clear it, and remove it"""
        if name in self._children:
            widget=self._children[name].widget
            IQContainer.remove_child(self,name)
            IQLayoutManagedWidget.remove_layout_element(self,widget)
        else:
            IQContainer.remove_child(self,name)
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
        IQContainer.clear(self)
        IQLayoutManagedWidget.clear(self)

class QWidgetContainer(IQWidgetContainer, QtWidgets.QWidget):
    """
    Generic widget container.

    Combines :class:`IQContainer` management of GUI values and timers
    with :class:`.IQLayoutManagedWidget` management of the contained widget's layout.

    Typically, adding widget adds them both to the container values and to the layout;
    however, this can be skipped by either using :meth:`.QLayoutManagedWidget.add_to_layout`
    (only add to the layout), or specifying ``location="skip"`` in :meth:`add_child` (only add to the container).
    
    Simply a combination of :class:`IQWidgetContainer` and ``QWidget``.
    """



class QFrameContainer(IQWidgetContainer, QtWidgets.QFrame):
    """An extension of :class:`IQWidgetContainer` for a ``QFrame`` Qt base class"""

class QDialogContainer(IQWidgetContainer, QtWidgets.QDialog):
    """An extension of :class:`IQWidgetContainer` for a ``QDialog`` Qt base class"""

class QGroupBoxContainer(IQWidgetContainer, QtWidgets.QGroupBox):
    """An extension of :class:`IQWidgetContainer` for a ``QGroupBox`` Qt base class"""
    def setup(self, caption=None, layout="vbox", no_margins=False, name=None):  # pylint: disable=arguments-differ, arguments-renamed
        super().setup(layout=layout,no_margins=no_margins,name=name)
        if caption is not None:
            self.setTitle(caption)

class QScrollAreaContainer(IQContainer, QtWidgets.QScrollArea):
    """
    An extension of :class:`IQWidgetContainer` for a ``QScrollArea`` Qt base class.
    
    Due to Qt organization, this container is "intermediate": it contains only a single :class:`QWidgetContainer` widget (named ``"widget"``),
    which in turn has all of the standard container traits: layout, multiple widgets, etc.
    Hence, when dealing with any container methods (adding children, changing layout, etc.), this widget (accessible with ``.widget()`` method) should be used.
    """
    class QContainedWidget(QWidgetContainer):
        @controller.exsafe
        def resizeEvent(self, event):
            scroll_container=getattr(self,"scroll_container",None)
            if scroll_container is not None:
                margins=scroll_container.getContentsMargins()
                if getattr(self,"hfix",False):
                    scroll_container.setMinimumWidth(self.minimumSizeHint().width()+scroll_container.verticalScrollBar().width()+margins[0]+margins[2])
                if getattr(self,"vfix",False):
                    scroll_container.setMinimumHeight(self.minimumSizeHint().height()+scroll_container.horizontalScrollBar().height()+margins[1]+margins[3])
            return super().resizeEvent(event)
    def setup(self, layout="vbox", no_margins=False, name=None, fix_width=True, fix_height=False):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Setup the container.

        `layout` specifies the container layout, `no_margins` determines whether margins within the container are removed,
        `name` specifies the widget name (if not specified yet).
        `fix_width` and `fix_height` determine whether the corresponding direction behaves as a scroll window (i.e., the size is fixed when the content changes),
        or as a standard widget container (the size is determined by the content).
        """
        super().setup(name=name)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setWidgetResizable(True)
        self._cont=self.QContainedWidget(self)
        self._cont.scroll_container=self
        self._cont.hfix=fix_width
        self._cont.vfix=fix_height
        self._cont.setup(layout=layout,no_margins=no_margins,name="widget")
        self.add_child("widget",self._cont)
        self.setWidget(self._cont)
    def clear(self):
        cont=self.widget()
        if cont is not None:
            cont.clear()



class QTabContainer(IQContainer, QtWidgets.QTabWidget):
    """
    Container which manages tab widget.

    Does not have its own layout, but can add or remove tabs, which are represented as :class:`QFrameContainer` widgets.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self._tabs={}
    def _insert_tab(self, tab, caption, index):
        if index is None:
            index=self.count()
        elif index<0:
            index=index%self.count()
        else:
            index=min(index,self.count())
        self.insertTab(index,tab,caption)
    def add_tab(self, name, caption, index=None, widget=None, layout="vbox", gui_values_path=True, no_margins=True):
        """
        Add a new tab container with the given `caption` to the widget.

        `index` specifies the new tab's index (``None`` means adding to the end, negative values count from the end).
        If `widget` is ``None``, create a new frame widget using the given `layout` (``"vbox"``, ``"hbox"``, or ``"grid"``)
        and `no_margins` (specifies whether the frame has inner margins) arguments;
        otherwise, use the supplied widget.
        The other parameters are the same as in :meth:`add_child` method.
        """
        if name in self._tabs:
            raise ValueError("tab {} already exists".format(name))
        if widget is None:
            widget=QFrameContainer(self)
            self.add_child(name=name,widget=widget,gui_values_path=gui_values_path)
            widget.setup(layout=layout,no_margins=no_margins)
        else:
            self.add_child(name=name,widget=widget,gui_values_path=gui_values_path)
        self._insert_tab(widget,caption,index)
        self._tabs[name]=widget
        return widget
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
    def get_current_name(self):
        """Get current tab name"""
        tab=self.currentWidget()
        for n,w in self._tabs.items():
            if tab is w:
                return n
    def set_by_name(self, name):
        """Set tab by name"""
        tab=self.c[name]
        self.setCurrentIndex(self.indexOf(tab))