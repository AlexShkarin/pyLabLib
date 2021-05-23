from ...core.gui.qt.thread import controller, threadprop
from ...core.gui.qt import values as values_module

from PyQt5 import QtCore

import collections

class IGUIController(QtCore.QObject):
    """
    Basic layout of a controller object which coordinates interaction between different widgets working on the same task.
    """
    def __init__(self):
        super(IGUIController, self).__init__()
        self.widgets_desc={}
        self.widgets={}
        self.ctl=controller.get_gui_controller()
        self.params_table=values_module.IndicatorValuesTable()

    TWidget=collections.namedtuple("TWidget",["params_path"])
    def add_widget_desc(self, name, params_path=None):
        """
        Add a widget description under a given name.

        If params_path` is not ``None``, it specifies path under which the widget is stored in the parameters' table
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
            self.params_table.add_widget(desc.params_path,widget)
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
        return self.params_table.get_all_values()
    def set_all_values(self, params):
        """Set all widget parameter values"""
        return self.params_table.set_all_values(params)
    def get_all_indicators(self):
        """Get all GUI indicators as a dictionary"""
        return self.params_table.get_all_indicators()