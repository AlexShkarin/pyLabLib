"""
Uniform representation of values from different widgets: numerical and text edits and labels, combo and check boxes, buttons.
"""

from .widgets import edit
from PyQt5 import QtCore, QtWidgets
from ...utils import dictionary, py3, string
from ...utils.functions import FunctionSignature
from .thread import controller


def build_children_tree(root, types_include, is_atomic=None, is_excluded=None, self_node="#"):
    is_atomic=is_atomic or (lambda _: False)
    is_excluded=is_excluded or (lambda _: False)
    children=dictionary.Dictionary()
    if not (is_atomic and is_atomic(root)):
        for ch in root.findChildren(QtCore.QObject):
            chn=str(ch.objectName())
            if (ch.parent() is root) and chn and not is_excluded(ch) and (chn not in children):
                children[str(ch.objectName())]=build_children_tree(ch,types_include,is_atomic,is_excluded,self_node)
        if isinstance(root,tuple(types_include)):
            children[self_node]=root
    else:
        children[self_node]=root
    return children


def has_methods(widget, methods_sets):
    """
    Chick if the widget has methods from given set.

    `methods_sets` is a list of method sets. The function returns ``True`` iff the widget has at least one method from each of the sets.
    """
    for ms in methods_sets:
        if not any([hasattr(widget,m) for m in ms]):
            return False
    return True

def get_method_kind(method, add_args=0):
    """
    Determine whether the method takes name as its argument

    `add_args` specifies number of additional required arguments.
    Return ``"named"`` is the method has at least ``add_args+1`` arguments, and the first one is called ``"name"``.
    Otherwise, return ``"simple"``.
    """
    if method is None:
        return None
    fsig=FunctionSignature.from_function(method)
    if len(fsig.arg_names)>=1+add_args and fsig.arg_names[0]=="name":
        return "named"
    else:
        return "simple"


class IValueHandler(object):
    """
    Generic handler of a widget value.

    Has method to get and set the value (or all values, if the widget has internal value structure), representing values as strings, and value changed signal.

    Args:
        widget: handled widget.
    """
    def __init__(self, widget):
        object.__init__(self)
        self.widget=widget
    def get_value(self, name=None):
        """
        Get widget value.

        If ``name`` is not ``None``, it specifies the name of the value parameter inside the widget (for complex widgets).
        """
        raise NotImplementedError("IValueHandler.get_value")
    def get_all_values(self):
        """
        Get all values of the widget.

        Return widget value for simple widgets, or a dictionary of all internal values for complex widgets.
        """
        return self.get_value()
    def set_value(self, value, name=None):
        """
        Set widget value.

        If ``name`` is not ``None``, it specifies the name of the value parameter inside the widget (for complex widgets).
        """
        raise NotImplementedError("IValueHandler.set_value")
    def set_all_values(self, value):
        """
        Set all values of the widget.

        `value` is a target value for simple widgets, or a dictionary of values for complex widgets.
        """
        return self.set_value(value)
    def repr_value(self, value, name=None):
        """
        Return textual representation of the value.

        If ``name`` is not ``None``, it specifies the name of the value parameter inside the widget (for complex widgets).
        """
        return str(value)
    def value_changed_signal(self):
        """
        Get the pyQt signal emitted when the value is changed.
        """
        if hasattr(self.widget,"value_changed"):
            return self.widget.value_changed
        return None


class VirtualValueHandler(IValueHandler):
    """
    Virtual value handler (to simulate controls which are not present in the GUI).

    Args:
        value: initial value
        complex_value (bool): if ``True``, the internal value is assumed to be complex, so it is forced to be a :class:`.Dictionary`.
    """
    def __init__(self, value=None, complex_value=False):
        IValueHandler.__init__(self,None)
        self.complex_value=complex_value
        self.value=dictionary.Dictionary(value) if complex_value else value
        self.value_changed=QtCore.pyqtSignal("PyQt_PyObject")
    def get_value(self, name=None):
        if name is None:
            return self.value
        else:
            return self.value[name]
    def set_value(self, value, name=None):
        if name is None:
            if self.complex_value:
                self.value=dictionary.Dictionary(value)
            else:
                self.value=value
        else:
            if name in self.value:
                del self.value[name]
            self.value[name]=value
        self.value_changed.emit(self.value)
    def value_changed_signal(self):
        return self.value_changed

_default_getters=("get_value","get_all_values")
_default_setters=("set_value","set_all_values")
class IDefaultValueHandler(IValueHandler):
    """
    Default value handler, typically used for custom widgets.

    To implement getting and setting values, looks for ``get/set_value`` and ``get/set_all_values`` methods for the widget and uses them accordingly.

    Args:
        widget: handled widget
        default_name(str): default name to be supplied to ``get/set_value`` and ``get/set_all_values`` methods if they require a name argument.
    """
    def __init__(self, widget, default_name=None):
        IValueHandler.__init__(self,widget)
        self.get_value_kind=get_method_kind(getattr(self.widget,"get_value",None))
        self.get_all_values_kind="simple" if hasattr(self.widget,"get_all_values") else None
        if not (self.get_value_kind or self.get_all_values_kind):
            raise ValueError("can't find default getter for widget {}".format(self.widget))
        self.set_value_kind=get_method_kind(getattr(self.widget,"set_value",None),add_args=1)
        self.set_all_values_kind="simple" if hasattr(self.widget,"set_all_values") else None
        if not (self.set_value_kind or self.set_all_values_kind):
            raise ValueError("can't find default setter for widget {}".format(self.widget))
        self.repr_value_kind=get_method_kind(getattr(self.widget,"repr_value",None),add_args=1)
        self.default_name=default_name
    def get_value(self, name=None):
        if not name:
            if self.get_value_kind=="simple":
                return self.widget.get_value()
            elif self.get_value_kind=="named":
                return self.widget.get_value(self.default_name)
            else:
                return self.widget.get_all_values()
        else:
            if self.get_value_kind=="named":
                return self.widget.get_value(name)
            elif self.get_all_values_kind=="simple":
                return self.widget.get_all_values()[name]
        raise ValueError("can't find getter for widget {} with name {}".format(self.widget,name))
    def get_all_values(self):
        if self.get_all_values_kind=="simple":
            return self.widget.get_all_values()
        elif self.get_value_kind=="simple":
            return self.widget.get_value()
        else:
            return self.widget.get_value(self.default_name)
    def set_value(self, value, name=None):
        if not name:
            if self.set_value_kind=="simple":
                return self.widget.set_value(value)
            elif self.set_value_kind=="named":
                return self.widget.set_value(self.default_name,value)
            else:
                return self.widget.set_all_values(value)
        else:
            if self.set_value_kind=="named":
                return self.widget.set_value(name,value)
            elif self.set_all_values_kind=="simple":
                if isinstance(name,list):
                    name="/".join(name)
                return self.widget.set_all_values({name:value})
        raise ValueError("can't find setter for widget {} with name {}".format(self.widget,name))
    def set_all_values(self, value):
        if self.set_all_values_kind=="simple":
            return self.widget.set_all_values(value)
        elif self.set_value_kind=="simple":
            return self.widget.set_value(value)
        else:
            return self.widget.set_value(self.default_name,value)
    def repr_value(self, value, name=None):
        if not name:
            if self.repr_value_kind=="simple":
                return self.widget.repr_value(value)
            elif self.repr_value_kind=="named":
                return self.widget.repr_value(self.default_name,value)
        else:
            if self.repr_value_kind=="named":
                return self.widget.repr_value(value)
        return str(value)

class ISingleValueHandler(IValueHandler):
    """
    Base class for single-value widget handler, typically used for built-in pyQt widgets.

    Defines new functions ``get/set_single_value`` which don't take a name argument; raises an error if the name is supplied to any of the standard functions. 

    Args:
        widget: handled widget
    """
    def __init__(self, widget):
        IValueHandler.__init__(self,widget)
    def get_single_value(self):
        """Get the widget value"""
        raise ValueError("can't find default getter for widget {}".format(self.widget))
    def get_value(self, name=None):
        """
        Get widget value.

        If ``name`` is not ``None`` raise an error.
        """
        if name:
            raise KeyError("no value with name {}".format(name))
        return self.get_single_value()
    def set_single_value(self, value):
        """Set the widget value"""
        raise ValueError("can't find default setter for widget {}".format(self.widget))
    def set_value(self, value, name=None):
        """
        Set widget value.

        If ``name`` is not ``None`` raise an error.
        """
        if name:
            raise KeyError("no value with name {}".format(name))
        return self.set_single_value(value)
    def repr_single_value(self, value):
        """Represent the widget value as a string"""
        if hasattr(self.widget,"repr_value"):
            return self.widget.repr_value(value)
        return str(value)
    def repr_value(self, value, name=None):
        """
        Return textual representation of the value.

        If ``name`` is not ``None`` raise an error.
        """
        if name:
            raise KeyError("no value with name {}".format(name))
        return self.repr_single_value(value)

class LineEditValueHandler(ISingleValueHandler):
    """Value handler for ``QLineEdit`` widget"""
    def get_single_value(self):
        return str(self.widget.text())
    def set_single_value(self, value):
        return self.widget.setText(str(value))
    def value_changed_signal(self):
        return self.widget.textChanged
class LabelValueHandler(ISingleValueHandler):
    """Value handler for ``QLabel`` widget"""
    def get_single_value(self):
        return str(self.widget.text())
    def set_single_value(self, value):
        return self.widget.setText(str(value))
class IBoolValueHandler(ISingleValueHandler):
    """Generic value handler for widgets with boolean values"""
    def __init__(self, widget, labels=("Off","On")):
        ISingleValueHandler.__init__(self,widget)
        self.labels=labels
    def repr_single_value(self, value):
        return self.labels[value]
class CheckboxValueHandler(IBoolValueHandler):
    """Value handler for ``QCheckBox`` widget"""
    def get_single_value(self):
        return self.widget.isChecked()
    def set_single_value(self, value):
        return self.widget.setChecked(value)
    def value_changed_signal(self):
        return self.widget.stateChanged
class PushButtonValueHandler(IBoolValueHandler):
    """Value handler for ``QPushButton`` widget"""
    def get_single_value(self):
        return self.widget.isChecked()
    def set_single_value(self, value):
        if self.widget.isCheckable():
            return self.widget.setChecked(value)
        elif value:
            return self.widget.click()
    def value_changed_signal(self):
        if self.widget.isCheckable():
            return self.widget.toggled
        else:
            return self.widget.clicked
    def repr_single_value(self, value):
        if not self.widget.isCheckable():
            return ""
        return IBoolValueHandler.repr_single_value(self,value)
class ToolButtonValueHandler(IBoolValueHandler):
    """Value handler for ``QToolButton`` widget"""
    def get_single_value(self):
        return self.widget.isChecked()
    def set_single_value(self, value):
        return self.widget.setChecked(value)
    def value_changed_signal(self):
        return self.widget.triggered
    def repr_single_value(self, value):
        if not self.widget.isCheckable():
            return ""
        return IBoolValueHandler.repr_single_value(self,value)
class ComboBoxValueHandler(ISingleValueHandler):
    """Value handler for ``QComboBox`` widget"""
    def get_single_value(self):
        return self.widget.currentIndex()
    def set_single_value(self, value):
        return self.widget.setCurrentIndex(value)
    def value_changed_signal(self):
        return self.widget.currentIndexChanged
    def repr_single_value(self, value):
        if isinstance(value,py3.anystring):
            return value
        return self.widget.itemText(value)
class ProgressBarValueHandler(ISingleValueHandler):
    """Value handler for ``QProgressBar`` widget"""
    def get_single_value(self):
        return self.widget.value()
    def set_single_value(self, value):
        return self.widget.setValue(int(value))

def is_handled_widget(widget):
    """Check if the widget can be handles by :class:`IDefaultValueHandler`"""
    return has_methods(widget,[_default_getters,_default_setters])

def get_default_value_handler(widget):
    """Autodetect value handler for the given widget"""
    if is_handled_widget(widget):
        return IDefaultValueHandler(widget)
    if isinstance(widget,QtWidgets.QLineEdit):
        return LineEditValueHandler(widget)
    if isinstance(widget,QtWidgets.QLabel):
        return LabelValueHandler(widget)
    if isinstance(widget,QtWidgets.QCheckBox):
        return CheckboxValueHandler(widget)
    if isinstance(widget,QtWidgets.QPushButton):
        return PushButtonValueHandler(widget)
    if isinstance(widget,(QtWidgets.QComboBox)):
        return ComboBoxValueHandler(widget)
    if isinstance(widget,QtWidgets.QProgressBar):
        return ProgressBarValueHandler(widget)
    return IValueHandler(widget)



class ValuesTable(object):
    """
    A table of values which can be used to manipulate many value handlers at once and represent them as a hierarchical structure.

    Has two container-like accessor:
    ``.v`` for settings/getting values
    (i.e., ``self.get_value(name)`` is equivalent to ``self.v[name]``, and ``self.set_value(name, value)`` is equivalent to ``self.v[name]=value``)
    and ``.w`` for getting the underlying widget
    (i.e., ``self.get_widget(name)`` is equivalent to ``self.w[name]``)

    Args:
        gui_thread_safe (bool): if ``True``, all value-access calls (``get/set_value``, ``get/set_all_values``)
            are automatically called in the GUI thread.
    """
    def __init__(self, gui_thread_safe=False):
        object.__init__(self)
        self.handlers=dictionary.Dictionary()
        self.gui_thread_safe=gui_thread_safe
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)
        self.w=dictionary.ItemAccessor(self.get_widget)

    def add_handler(self, name, handler):
        """Add a value handler under a given name"""
        self.handlers[name]=handler
        return handler
    def remove_handler(self, name):
        """Remove the value handler with a given name"""
        del self.handlers[name]
    def get_handler(self, name):
        """Get the value hander with the given name"""
        return self.handlers[name]

    def __getitem__(self, name):
        return self.get_handler(name)
    def __setitem__(self, name, value):
        return self.add_handler(name,value)
    def __delitem__(self, name):
        return self.remove_handler(name)
    def __contains__(self, name):
        return name in self.handlers

    def add_widget(self, name, widget):
        """Add a widget under a given name (value handler type is auto-detected)"""
        return self.add_handler(name,get_default_value_handler(widget))
    def get_widget(self, name):
        """Get the widget corresponding to the handler under the given name"""
        return self.get_handler(name).widget
    def add_table(self, name, table):
        """Add a nested :class:`ValuesTable` under a given name"""
        return self.add_handler(name,IDefaultValueHandler(table))
    def add_virtual_element(self, name, value=None):
        """
        Add a virtual value element.

        Doesn't correspond to any actual widget, but behaves very similarly from the application point of view
        (its value can be set or read, it has on-change events, it can have indicator).
        """
        return self.add_handler(name,VirtualValueHandler(value))
    _default_value_types=(edit.LVTextEdit,edit.LVNumEdit,QtWidgets.QLineEdit,QtWidgets.QCheckBox,QtWidgets.QPushButton,QtWidgets.QComboBox)
    def add_all_children(self, root, root_name=None, types_include=None, types_exclude=(), names_exclude=None):
        """
        Add a widget and all its children to the table.

        Args:
            root: root widget
            root_name: path to the sub-branch where the values will be placed
            types_include: if not ``None``, specifies list of widget classes to include in the table
            types_include: specifies list of widget classes to exclude from the table
            names_exclude: if not ``None``, specifies list of widget names to exclude from the table
        """
        name_filt=string.sfregex(exclude=names_exclude)
        def is_excluded(w):
            return isinstance(w,types_exclude) or not name_filt(str(w.objectName()))
        types_include=types_include or self._default_value_types
        tree=build_children_tree(root,types_include,is_atomic=is_handled_widget,is_excluded=is_excluded)
        for path,widget in tree.iternodes(include_path=True):
            if path[-1]=="#":
                path=path[:-1]
                if root_name is not None:
                    path=[root_name]+path[1:]
                name="/".join([p for p in path if p])
                self.add_widget(name,widget)

    @controller.gui_thread_method
    def get_value(self, name):
        """
        Get value under a given name.

        Automatically handles complex widgets and sub-names
        """
        path,subpath=self.handlers.get_max_prefix(name,kind="leaf")
        if path is None:
            raise KeyError("missing handler {}".format(name))
        return self.handlers[path].get_value(subpath)
    @controller.gui_thread_method
    def get_all_values(self, root="", include=None):
        """
        Get all values in a subtree with the given root (all table values by default).
        
        If supplied, `include` is a container specifies which specifies names (relative to the root) to include in the result; by default, include everything.
        Return a :class:`.Dictionary` object containing tree structure of the names.
        """
        values=dictionary.Dictionary()
        if root in self.handlers:
            for n in self.handlers[root].paths():
                if (include is None) or ("/".join(n) in include):
                    values[n]=self.handlers[(root,n)].get_all_values()
        return values
    @controller.gui_thread_method
    def set_value(self, name, value):
        """
        Set value under a given name.

        Automatically handles complex widgets and sub-names
        """
        path,subpath=self.handlers.get_max_prefix(name,kind="leaf")
        if path is None:
            raise KeyError("missing handler {}".format(name))
        return self.handlers[path].set_value(value,subpath)
    @controller.gui_thread_method
    def set_all_values(self, values, root="", include=None):
        """
        Set all values in a subtree with the given root (all table values by default).
        
        `values` is a dictionary with values (can only contain some values out of the ones the table).
        If supplied, `include` is a container specifies which specifies names (relative to the root) to include in the result; by default, include everything.
        """
        for n,v in dictionary.as_dictionary(values).iternodes(to_visit="all",topdown=True,include_path=True):
            if self.handlers.has_entry((root,n),kind="leaf"):
                if (include is None) or ("/".join(n) in include):
                    self.handlers[root,n].set_all_values(v)
            
    def repr_value(self, name, value):
        """
        Get a textual representation of a value under a given name.

        Automatically handles complex widgets and sub-names
        """
        path,subpath=self.handlers.get_max_prefix(name,kind="leaf")
        if path is None:
            raise KeyError("missing handler {}".format(name))
        return self.handlers[path].repr_value(value,subpath)
    def changed_event(self, name):
        """Get changed events for a value under a given name."""
        return self.handlers[name].value_changed_signal()
    def update_value(self, name):
        """Send update signal for a handler with a given name (emit a changed signal with the current value)"""
        changed_event=self.handlers[name].value_changed_signal()
        if changed_event:
            changed_event.emit(self.get_value(name))






class IIndicatorHandler(object):
    """
    Generic handler of an indicator.

    Has methods to get and set the indicator value.
    """
    def get_value(self, name=None):
        """
        Get indicator value.

        If ``name`` is not ``None``, it specifies the name of the indicator parameter inside the widget (for complex widgets).
        """
        raise NotImplementedError("IIndicatorHandler.get_value")
    def set_value(self, value, name=None):
        """
        Set indicator value.

        If ``name`` is not ``None``, it specifies the name of the indicator parameter inside the widget (for complex widgets).
        """
        raise NotImplementedError("IIndicatorHandler.set_value")

VirtualIndicatorHandler=VirtualValueHandler
_default_indicator_getters=("get_indicator","get_all_indicators")
_default_indicator_setters=("set_indicator","set_all_indicators")
class IDefaultIndicatorHandler(IIndicatorHandler):
    """
    Default indicator handler, typically used for custom widgets.

    To implement getting and setting values, looks for ``get/set_indicator`` methods for the widget and uses them accordingly.

    Args:
        widget: handled widget
        default_name(str): default name to be supplied to ``get/set_indicator`` methods if they require a name argument.
    """
    def __init__(self, widget, default_name=None):
        IIndicatorHandler.__init__(self)
        self.widget=widget
        self.get_indicator_kind=get_method_kind(getattr(self.widget,"get_indicator",None))
        self.get_all_indicators_kind="simple" if hasattr(self.widget,"get_all_indicators") else None
        self.set_indicator_kind=get_method_kind(getattr(self.widget,"get_indicator",None),add_args=1)
        self.set_all_indicators_kind="simple" if hasattr(self.widget,"set_all_indicators") else None
        self.default_name=default_name
    def get_value(self, name=None):
        if not (self.get_indicator_kind or self.get_all_indicators_kind):
            raise ValueError("can't find default indicator getter for widget {}".format(self.widget))
        if not name:
            if self.get_indicator_kind=="simple":
                return self.widget.get_indicator()
            elif self.get_indicator_kind=="named":
                return self.widget.get_indicator(self.default_name)
            else:
                return self.widget.get_all_indicators()
        else:
            if self.get_indicator_kind=="named":
                return self.widget.get_indicator()
            elif self.get_all_indicators_kind=="simple":
                return self.widget.get_all_indicators()[name]
        raise ValueError("can't find indicator getter for widget {} with name {}".format(self.widget,name))
    def set_value(self, value, name=None):
        if not (self.set_indicator_kind or self.set_all_indicators_kind):
            raise ValueError("can't find default indicator setter for widget {}".format(self.widget))
        if not name:
            if self.set_indicator_kind=="simple":
                return self.widget.set_indicator(value)
            elif self.set_indicator_kind=="named":
                return self.widget.set_indicator(self.default_name,value)
            else:
                return self.widget.set_all_indicators(value)
        else:
            if self.set_indicator_kind=="named":
                return self.widget.set_indicator(name,value)
            elif self.set_all_indicators_kind=="simple":
                if isinstance(name,list):
                    name="/".join(name)
                return self.widget.set_all_indicators({name:value})
        raise ValueError("can't find indicator setter for widget {} with name {}".format(self.widget,name))
class FuncLabelIndicatorHandler(IIndicatorHandler):
    """
    Indicator handler which uses a label to show the value.

    To takes optional function which converts values into strings (by default, use the standard string conversion).

    Args:
        label: widget or value hander used to represent the value (takes string values)
        repr_func: if not ``None``, specifies function used to convert values into strings
        repr_value_name(str): default name to be supplied to `repr_func` if it requires a name argument and name is not supplied.
    """
    def __init__(self, label, repr_func=None, repr_value_name=None):
        IIndicatorHandler.__init__(self)
        if not isinstance(label,IValueHandler):
            label=get_default_value_handler(label)
        self.label_handler=label
        self.repr_func=repr_func
        self.repr_func_kind=get_method_kind(repr_func,add_args=1)
        self.repr_value_name=repr_value_name
    def get_value(self, name=None):
        if name:
            raise KeyError("no indicator value with name {}".format(name))
        return self.label_handler.get_value()
    def repr_value(self, value, name=None):
        """Represent a value with a given name"""
        if name is None:
            if self.repr_func_kind is None:
                return str(value)
            elif self.repr_func_kind=="simple":
                return self.repr_func(value)
            else:
                return self.repr_func(self.repr_value_name,value)
        elif self.repr_func_kind=="named":
            return self.repr_func(name,value)
        raise KeyError("no indicator value with name {}".format(name))
    def set_value(self, value, name=None):
        return self.label_handler.set_value(self.repr_value(value,name=name))
class WidgetLabelIndicatorHandler(IIndicatorHandler):
    """
    Indicator handler which uses a label to show the value.

    To takes optional widget or widget handler which converts values into strings using its ``repr_value`` method
    (by default, use the standard string conversion).

    Args:
        label: widget or value hander used to represent the value (takes string values)
        widget: if not ``None``, specifies widget used to convert values into strings
        repr_value_name(str): default name to be supplied to `repr_value` if it requires a name argument and name is not supplied.
    """
    def __init__(self, label, widget=None, repr_value_name=None):
        IIndicatorHandler.__init__(self)
        if not isinstance(label,IValueHandler):
            label=get_default_value_handler(label)
        self.label_handler=label
        if widget and not isinstance(widget,IValueHandler):
            widget=get_default_value_handler(widget)
        self.widget_handler=widget
        self.repr_value_name=repr_value_name
    def get_value(self, name=None):
        if name:
            raise KeyError("no indicator value with name {}".format(name))
        return self.label_handler.get_value()
    def repr_value(self, value, name=None):
        """Represent a value with a given name"""
        if self.widget_handler:
            return self.widget_handler.repr_value(value,name=self.repr_value_name if name is None else name)
        if name:
            raise KeyError("no indicator value with name {}".format(name))
        return str(value)
    def set_value(self, value, name=None):
        return self.label_handler.set_value(self.repr_value(value,name=name))

def get_default_indicator_handler(widget, label=None, require_setter=False):
    """Autodetect indicator handler for the given widget and label"""
    if label is not None:
        return WidgetLabelIndicatorHandler(label,widget)
    if has_methods(widget,[_default_indicator_getters]):
        if (not require_setter) or has_methods(widget,[_default_indicator_setters]):
            return IDefaultIndicatorHandler(widget)
    return None


class IndicatorValuesTable(ValuesTable):
    """
    A table of values which can also handle indicators. Inherits :class:`ValuesTable`

    Has an additional container-like accessor ``.i`` for settings/getting indicator values
    (i.e., ``self.get_indicator(name)`` is equivalent to ``self.i[name]``, and ``self.set_indicator(name, value)`` is equivalent to ``self.i[name]=value``)

    Args:
        gui_thread_safe (bool): if ``True``, all value-access and indicator-access calls
            (``get/set_value``, ``get/set_all_values``, ``get/set_indicator``, ``get/set_all_indicators``, and ``update_indicators``)
            are automatically called in the GUI thread.
    """
    def __init__(self, gui_thread_safe=False):
        ValuesTable.__init__(self,gui_thread_safe=gui_thread_safe)
        self.indicator_handlers=dictionary.Dictionary()
        self.i=dictionary.ItemAccessor(self.get_indicator,self.set_indicator)
    def add_indicator_handler(self, name, handler, ind_name="__default__"):
        """
        Add indicator handler with a given name.

        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        """
        if handler is not None:
            self.indicator_handlers[name,ind_name]=handler
            return handler
        return None
    def remove_indicator_handler(self, name, ind_name=None):
        """
        Remove indicator handler with a given name.

        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        By default, remove all indicators with this name
        """
        if ind_name is None:
            del self.indicator_handlers[name]
        else:
            del self.indicator_handlers[name,ind_name]
    def add_widget_indicator(self, name, widget, label=None, ind_name="__default__"):
        """
        Add widget-based indicator with a given name.

        If ``label`` is ``None``, use widget's ``set_indicator`` and ``get_indicator`` functions to indicate the value.
        Otherwise, use :class:`WidgetLabelIndicatorHandler` with the given label (`label` is used to show the value, `widget` is used to represent it).
        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        """
        return self.add_indicator_handler(name,get_default_indicator_handler(widget,label),ind_name=ind_name)
    def add_label_indicator(self, name, label, repr_func=None, ind_name="__default__"):
        """
        Add label-based indicator with a given name.

        `repr_func` can specify representation function which turns values into text.
        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        """
        return self.add_indicator_handler(name,FuncLabelIndicatorHandler(label,repr_func=repr_func),ind_name=ind_name)
    def add_widget(self, name, widget):
        h=ValuesTable.add_widget(self,name,widget)
        self.add_indicator_handler(name,IDefaultIndicatorHandler(widget))
        return h
    def add_virtual_element(self, name, value=None):
        h=ValuesTable.add_virtual_element(self,name,value=value)
        self.add_indicator_handler(name,VirtualIndicatorHandler(value))
        return h
    def add_table(self, name, table):
        h=ValuesTable.add_table(self,name,table)
        self.add_indicator_handler(name,IDefaultIndicatorHandler(table))
        return h

    @controller.gui_thread_method
    def get_indicator(self, name, ind_name="__default__"):
        """
        Get indicator value with a given name.

        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        """
        path,subpath=self.indicator_handlers.get_max_prefix(name)
        epath=path+[ind_name] if (ind_name and path is not None) else path
        if path is None or (len(subpath)>0 and not self.indicator_handlers.has_entry(epath,kind="leaf")):
            raise KeyError("missing handler {}".format(name))
        args=[subpath] if len(subpath) else []
        return self.indicator_handlers[epath].get_value(*args)
    @controller.gui_thread_method
    def get_all_indicators(self, root="", ind_name="__default__", include=None):
        """
        Get all indicator values in a subtree with the given root (all table values by default).
        
        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        If supplied, `include` is a container specifies which specifies names (relative to the root) to include in the result; by default, include everything.
        Return a :class:`.Dictionary` object containing tree structure of the names.
        """
        values=dictionary.Dictionary()
        if root in self.handlers:
            for n in self.handlers[root].paths():
                if (include is None) or ("/".join(n) in include):
                    try:
                        values[n]=self.get_indicator(n,ind_name=ind_name)
                    except (KeyError, ValueError):
                        pass
        return values
    @controller.gui_thread_method
    def set_indicator(self, name, value, ind_name=None):
        """
        Set indicator value with a given name.

        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        By default, set all sub-indicators to the given value.
        """
        path,subpath=self.indicator_handlers.get_max_prefix(name)
        epath=path+[ind_name] if (ind_name and path is not None) else path
        if path is None:
            raise KeyError("missing handler {}".format(name))
        args=[value,subpath] if len(subpath) else [value]
        if ind_name is None:
            for i in self.indicator_handlers[path].iternodes():
                i.set_value(*args)
        else:
            return self.indicator_handlers[epath].set_value(*args)
    @controller.gui_thread_method
    def set_all_indicators(self, values, root="", include=None):
        """
        Set all indicator values in a subtree with the given root (all table values by default).
        
        `values` is a dictionary with indicated values (can only contain some values out of the ones the table).
        If supplied, `include` is a container specifies which specifies names (relative to the root) to include in the result; by default, include everything.
        """
        for n,v in dictionary.as_dictionary(values).iternodes(include_path=True):
            if self.indicator_handlers.has_entry((root,n,"__default__"),kind="leaf"):
                if (include is None) or ("/".join(n) in include):
                    try:
                        self.set_indicator((root,n),v)
                    except ValueError:
                        pass
    @controller.gui_thread_method
    def update_indicators(self, root="", include=None):
        """
        Update all indicators in a subtree with the given root (all table values by default) to represent current values.
        If supplied, `include` is a container specifies which specifies names (relative to the root) to include in the result; by default, include everything.
        """
        for n in self.handlers[root].paths():
            if (include is None) or ("/".join(n) in include):
                p=(root,n)
                if p in self.indicator_handlers:
                    try:
                        self.set_indicator(p,self.get_value(p))
                    except ValueError:
                        pass