from ..core.thread import controller
from ..core.gui import value_handling

from PyQt5 import QtCore

import collections

class IGUIController(QtCore.QObject):
    """
    Basic layout of a controller object which coordinates interaction between different widgets working on the same task.
    """
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.widgets_desc={}
        self.widgets={}
        self.ctl=controller.get_gui_controller()
        self.gui_values=value_handling.GUIValues()

    TWidget=collections.namedtuple("TWidget",["params_path"])
    def add_widget_desc(self, name, params_path=None):
        """
        Add a widget description under a given name.

        If `params_path` is not ``None``, it specifies path under which the widget is stored in the parameters' table
        (by default, same as the widget's name).
        """
        self.widgets_desc[name]=self.TWidget(params_path)
    def set_widget(self, name, widget):
        """
        Set the widget with the given name.

        Description with the given name should be created beforehand (see :meth:`add_widget_desc`).
        """
        self.widgets[name]=widget
        desc=self.widgets_desc.setdefault(name,self.TWidget(None))
        if desc.params_path is not None:
            self.gui_values.add_widget(desc.params_path,widget)
    def get_widget(self, name, default=None):
        """
        Get the widget with the given name
        """
        return self.widgets.get(name,default)
    __getitem__=get_widget
    def __contains__(self, name):
        return name in self.widgets
    
    def get_all_values(self):
        """Get all widget parameter values"""
        return self.gui_values.get_all_values()
    def set_all_values(self, values):
        """Set all widget parameter values"""
        return self.gui_values.set_all_values(values)
    def get_all_indicators(self):
        """Get all GUI indicators as a dictionary"""
        return self.gui_values.get_all_indicators()