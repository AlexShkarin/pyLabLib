"""
Uniform representation of values from different widgets: numerical and text edits and labels, combo and check boxes, buttons.
"""

from .widgets import edit
from ..utils import dictionary, py3, string, functions as func_utils
from ..utils.functions import FunctionSignature
from ..thread.controller import gui_thread_method

from PyQt5 import QtCore, QtWidgets
import collections



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







class IValueHandler:
    """
    Generic handler of a widget value.

    Has method to get and set the value (or all values, if the widget has internal value structure), representing values as strings, and value changed signal.

    Args:
        widget: handled widget.
    """
    def __init__(self, widget):
        self.widget=widget
        self._change_handlers=[]
    def get_value(self, name=None):
        """
        Get widget value.

        If ``name`` is not ``None``, it specifies the name of the value parameter inside the widget (for complex widgets).
        """
        raise NotImplementedError("IValueHandler.get_value")
    def set_value(self, value, name=None):
        """
        Set widget value.

        If ``name`` is not ``None``, it specifies the name of the value parameter inside the widget (for complex widgets).
        """
        raise NotImplementedError("IValueHandler.set_value")
    def repr_value(self, value, name=None):
        """
        Return textual representation of the value.

        If ``name`` is not ``None``, it specifies the name of the value parameter inside the widget (for complex widgets).
        """
        return str(value)
    def value_changed(self):
        """
        Get the pyQt signal emitted when the value is changed.
        """
        if hasattr(self.widget,"value_changed"):
            return self.widget.value_changed
        return None
    def connect_value_changed_handler(self, handler, only_signal=True):
        """
        Connect value changed signal.

        If ``only_signal==True``, equivalent to connecting a handler function to :meth:`value_changed` signal;
        however, if ``only_signal==False``, it also works for some objects (e.g., ``QLabel``) don't have built-in on-changed signals
        by calling the handler explicitly every time the value is changed.

        Note that the connection is always direct (i.e., it doesn't deal with message queues and different threads, but rather directly calls the handler function).
        If you need to connect a handler to a signal using some other connection method, you can use :meth:`value_changed` directly.
        """
        signal=self.value_changed()
        if signal is not None:
            signal.connect(handler,QtCore.Qt.DirectConnection)
        elif not only_signal:
            self._change_handlers.append(handler)
    def _notify_value_changed_handlers(self, value):
        """Notify emulated value changed handlers"""
        for h in self._change_handlers:
            func_utils.call_cut_args(h,value)
    _focused_set_allowed=False
    def can_set_value(self, allow_focus=True):
        """
        Check if setting value from the code is allowed.

        Args:
            focus: if ``False``, indicates that settings of focused widgets isn't allowed, with some exceptions (buttons, check boxes, combo boxes)
        """
        if (not self._focused_set_allowed) and (not allow_focus) and hasattr(self.widget,"hasFocus") and self.widget.hasFocus():
            return False
        return True


class VirtualValueHandler(IValueHandler):
    """
    Virtual value handler (to simulate controls which are not present in the GUI).

    Args:
        value: initial value
        multivalued (bool): if ``True``, the internal value is assumed to be complex, so it is forced to be a :class:`.Dictionary` every time it is set.
    """
    def __init__(self, value=None, multivalued=False):
        IValueHandler.__init__(self,None)
        self.multivalued=multivalued
        self.value=dictionary.Dictionary(value) if multivalued else value
    def get_value(self, name=None):
        if name is None:
            return self.value
        else:
            return self.value[name]
    def set_value(self, value, name=None):
        if name is None:
            if self.multivalued:
                self.value=dictionary.Dictionary(value)
            else:
                self.value=value
        else:
            if name in self.value:
                del self.value[name]
            self.value[name]=value
        self._notify_value_changed_handlers(value)



_default_getters=("get_value","get_all_values")
_default_setters=("set_value","set_all_values")
class StandardValueHandler(IValueHandler):
    """
    Standard value handler, typically used for custom widgets.

    To implement getting and setting values, looks for ``get/set_value`` and ``get/set_all_values`` methods for the widget and uses them accordingly.
    To implement value representing, looks for ``repr_value`` method (if not defined, use simple string conversion).
    To implement value change signal, looks for ``value_changed`` widget signal.

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
        if name is None:
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
    def set_value(self, value, name=None):
        if name is None:
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
    def repr_value(self, value, name=None):
        if name is None:
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
    def value_changed(self):
        return self.widget.textChanged
class LabelValueHandler(ISingleValueHandler):
    """Value handler for ``QLabel`` widget"""
    _focused_set_allowed=True
    def get_single_value(self):
        return str(self.widget.text())
    def set_single_value(self, value):
        value=str(value)
        self._notify_value_changed_handlers(value)
        return self.widget.setText(value)
class IBoolValueHandler(ISingleValueHandler):
    """Generic value handler for widgets with boolean values"""
    def __init__(self, widget, labels=("Off","On")):
        ISingleValueHandler.__init__(self,widget)
        self.labels=labels
    def repr_single_value(self, value):
        return self.labels[value]
class CheckboxValueHandler(IBoolValueHandler):
    """Value handler for ``QCheckBox`` widget"""
    _focused_set_allowed=True
    def get_single_value(self):
        return self.widget.isChecked()
    def set_single_value(self, value):
        return self.widget.setChecked(value)
    def value_changed(self):
        return self.widget.stateChanged
class PushButtonValueHandler(IBoolValueHandler):
    """Value handler for ``QPushButton`` widget"""
    _focused_set_allowed=True
    def get_single_value(self):
        return self.widget.isChecked()
    def set_single_value(self, value):
        if self.widget.isCheckable():
            return self.widget.setChecked(value)
        elif value:
            return self.widget.click()
    def value_changed(self):
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
    _focused_set_allowed=True
    def get_single_value(self):
        return self.widget.isChecked()
    def set_single_value(self, value):
        return self.widget.setChecked(value)
    def value_changed(self):
        return self.widget.triggered
    def repr_single_value(self, value):
        if not self.widget.isCheckable():
            return ""
        return IBoolValueHandler.repr_single_value(self,value)
class ComboBoxValueHandler(ISingleValueHandler):
    """Value handler for ``QComboBox`` widget"""
    _focused_set_allowed=True
    def get_single_value(self):
        return self.widget.currentIndex()
    def set_single_value(self, value):
        return self.widget.setCurrentIndex(value)
    def value_changed(self):
        return self.widget.currentIndexChanged
    def repr_single_value(self, value):
        if isinstance(value,py3.anystring):
            return value
        return self.widget.itemText(value)
class ProgressBarValueHandler(ISingleValueHandler):
    """Value handler for ``QProgressBar`` widget"""
    _focused_set_allowed=True
    def get_single_value(self):
        return self.widget.value()
    def set_single_value(self, value):
        self._notify_value_changed_handlers(int(value))
        return self.widget.setValue(int(value))




def is_handled_widget(widget):
    """Check if the widget can be handles by :class:`StandardValueHandler`"""
    return has_methods(widget,[_default_getters,_default_setters])

def create_value_handler(widget):
    """Autodetect value handler for the given widget"""
    if is_handled_widget(widget):
        return StandardValueHandler(widget)
    if isinstance(widget,QtWidgets.QLineEdit):
        return LineEditValueHandler(widget)
    if isinstance(widget,QtWidgets.QLabel):
        return LabelValueHandler(widget)
    if isinstance(widget,QtWidgets.QCheckBox):
        return CheckboxValueHandler(widget)
    if isinstance(widget,QtWidgets.QPushButton):
        return PushButtonValueHandler(widget)
    if isinstance(widget,QtWidgets.QComboBox):
        return ComboBoxValueHandler(widget)
    if isinstance(widget,QtWidgets.QProgressBar):
        return ProgressBarValueHandler(widget)
    return IValueHandler(widget)









class IIndicatorHandler:
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
class StandardIndicatorHandler(IIndicatorHandler):
    """
    Default indicator handler, typically used for custom widgets.

    To implement getting and setting values, looks for ``get/set_indicator`` and ``get/set_all_indicators`` methods for the widget and uses them accordingly.

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
        if name is None:
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
        if name is None:
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
class LabelIndicatorHandler(IIndicatorHandler):
    """
    Indicator handler which uses a label to show the value.

    Can takes optional widget or widget handler which converts values into strings using its ``repr_value`` method
    (by default, use the standard string conversion).

    Args:
        label: widget or value hander used to represent the value (takes string values)
        formatter: specifies a way to turn values into string representation;
            can be a widget handler or a widget (its ``repr_func`` method is used to represent its value),
            a function (it takes either a single value argument or two arguments ``name`` and ``value`` and returns string value),
            or ``None`` (use simple string conversion)
        repr_value_name(str): default name to be supplied to `repr_value` if it requires a name argument and name is not supplied
    """
    def __init__(self, label, formatter=None, repr_value_name=None):
        IIndicatorHandler.__init__(self)
        if not isinstance(label,IValueHandler):
            label=create_value_handler(label)
        self.label_handler=label
        self.repr_value_name=repr_value_name
        self.widget_handler=None
        self.repr_func=None
        if isinstance(formatter,IValueHandler):
            self.widget_handler=formatter
        elif isinstance(formatter,QtWidgets.QWidget):
            self.widget_handler=create_value_handler(formatter)
        elif hasattr(formatter,"__call__"):
            self.repr_func=formatter
            self.repr_func_kind=get_method_kind(formatter,add_args=1)
        elif formatter is not None:
            raise ValueError("can't determine kind of formatter: {}".format(formatter))
    def get_value(self, name=None):
        if name:
            raise KeyError("no indicator value with name {}".format(name))
        return self.label_handler.get_value()
    def repr_value(self, value, name=None):
        """Represent a value with a given name"""
        if self.widget_handler is not None:
            return self.widget_handler.repr_value(value,name=self.repr_value_name if name is None else name)
        elif self.repr_func is not None:
            if name is None:
                if self.repr_func_kind=="simple":
                    return self.repr_func(value)
                else:
                    return self.repr_func(self.repr_value_name,value)
            elif self.repr_func_kind=="named":
                return self.repr_func(name,value)
        if name:
            raise KeyError("no indicator value with name {}".format(name))
        return str(value)
    def set_value(self, value, name=None):
        return self.label_handler.set_value(self.repr_value(value,name=name))

def create_indicator_handler(widget, label=None, require_setter=False):
    """Autodetect indicator handler for the given widget and optional indicator label"""
    if label is not None:
        return LabelIndicatorHandler(label,widget)
    if has_methods(widget,[_default_indicator_getters]):
        if (not require_setter) or has_methods(widget,[_default_indicator_setters]):
            return StandardIndicatorHandler(widget)
    return None








class GUIValues:
    """
    A collection of values which can be used to manipulate many value handlers at once and represent them as a hierarchical structure.

    Has four container-like accessor:
    ``.h`` for getting/adding/removing the value handler
    (i.e., ``self.get_handler(name)`` is equivalent to ``self.h[name]``, and ``self.add_handler(name, handler)`` is equivalent to ``self.h[name]=handler``,
    and ``self.remove_handler(name)`` is equivalent to ``del self.h[name]``),
    ``.w`` for getting the underlying widget
    (i.e., ``self.get_widget(name)`` is equivalent to ``self.w[name]``),
    ``.v`` for settings/getting values
    (i.e., ``self.get_value(name)`` is equivalent to ``self.v[name]``, and ``self.set_value(name, value)`` is equivalent to ``self.v[name]=value``),
    ``.i`` for settings/getting indicator values
    (i.e., ``self.get_indicator(name)`` is equivalent to ``self.i[name]``, and ``self.set_indicator(name, value)`` is equivalent to ``self.i[name]=value``)

    Args:
        gui_thread_safe (bool): if ``True``, all value-access and indicator-access calls
            (``get/set_value``, ``get/set_all_values``, ``get/set_indicator``, ``get/set_all_indicators``, and ``update_indicators``)
            are automatically called in the GUI thread.
    """
    def __init__(self, gui_thread_safe=True):
        self.gui_thread_safe=gui_thread_safe
        self.handlers=dictionary.Dictionary()
        self.indicator_handlers=dictionary.Dictionary()
        self.h=dictionary.ItemAccessor(self.get_handler,self.add_handler,self.remove_handler,contains_checker=self.__contains__)
        self.w=dictionary.ItemAccessor(self.get_widget,contains_checker=self.__contains__)
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value,contains_checker=self.__contains__)
        self.i=dictionary.ItemAccessor(self.get_indicator,self.set_indicator)

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

    def __contains__(self, name):
        return name in self.handlers

    def add_widget(self, name, widget, add_indicator=True):
        """Add a widget under a given name (value handler type is auto-detected)"""
        h=self.add_handler(name,create_value_handler(widget))
        if add_indicator:
            self.add_indicator_handler(name,create_indicator_handler(widget))
        return h
    def get_widget(self, name):
        """Get the widget corresponding to the handler under the given name"""
        return self.get_handler(name).widget
    def add_nested(self, name, gui_values, add_indicator=True):
        """Add a nested :class:`GUIValues` under a given name"""
        h=self.add_handler(name,StandardValueHandler(gui_values))
        if add_indicator:
            self.add_indicator_handler(name,StandardIndicatorHandler(gui_values))
        return h
    def add_virtual_element(self, name, value=None, multivalued=False, add_indicator=True):
        """
        Add a virtual value element.

        Doesn't correspond to any actual widget, but behaves very similarly from the application point of view
        (its value can be set or read, it has on-change events, it can have indicator).
        If ``add_indicator==True``, add default indicator handler as well.
        """
        h=self.add_handler(name,VirtualValueHandler(value,multivalued=multivalued))
        if add_indicator:
            self.add_indicator_handler(name,VirtualIndicatorHandler(value))
        return h
    _default_value_types=(edit.TextEdit,edit.NumEdit,QtWidgets.QLineEdit,QtWidgets.QCheckBox,QtWidgets.QPushButton,QtWidgets.QComboBox,QtWidgets.QProgressBar)
    def add_all_children(self, root, root_name=None, types_include=None, types_exclude=(), names_exclude=None):
        """
        Add a widget and all its children to the values set.

        The result is organized as a tree using parent-child relations (note that it implies that only children widgets correspond to tree nodes,
        i.e., only their values can be get/set).

        Args:
            root: root widget
            root_name: path to the sub-branch where the values will be placed
            types_include: if not ``None``, specifies list of widget classes (e.g., ``QCheckBox``) to include
            types_include: specifies list of widget classes to exclude
            names_exclude: if not ``None``, specifies list of widget names to exclude
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

    TIndicatorsSet=collections.namedtuple("TIndicatorsSet",["ind"])
    def add_indicator_handler(self, name, handler, ind_name="__default__"):
        """
        Add indicator handler with a given name.

        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        """
        if handler is not None:
            self.indicator_handlers.setdefault(name,self.TIndicatorsSet({})).ind[ind_name]=handler
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
        elif name in self.indicator_handlers:
            ind_set=self.indicator_handlers[name].ind
            if ind_name in ind_set:
                del ind_set[ind_name]
                if not ind_set:
                    del self.indicator_handlers[name]
    def add_widget_indicator(self, name, widget, label=None, ind_name="__default__"):
        """
        Add widget-based indicator with a given name.

        If ``label`` is ``None``, use widget's ``get/set_indicator`` or ``get/set_all_indicators`` functions to indicate the value.
        Otherwise, use the given label to indicate the value (`label` is used to show the value, `widget` is used to represent it).
        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        """
        return self.add_indicator_handler(name,create_indicator_handler(widget,label=label),ind_name=ind_name)
    def add_label_indicator(self, name, label, formatter=None, ind_name="__default__"):
        """
        Add label-based indicator with a given name.

        `formatter` specifies a way to turn values into string representation;
        can be a widget handler or a widget (its ``repr_func`` method is used to represent its value),
        a function (it takes either a single value argument or two arguments ``name`` and ``value`` and returns string value),
        or ``None`` (use simple string conversion)
        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        """
        return self.add_indicator_handler(name,LabelIndicatorHandler(label,formatter=formatter),ind_name=ind_name)

    @gui_thread_method
    def get_value(self, name=None, include=None):
        """
        Get a value or a set of values in a subtree under a given name (all values by default).

        Automatically handles complex widgets and sub-names.
        If `name` refers to a branchm return a :class:`.Dictionary` object containing tree structure of the names.
        If supplied, `include` is a container specifies which specifies names (relative to the root) to include in the result; by default, include everything.
        """
        name=name or ""
        path,subpath=self.handlers.get_max_prefix(name,kind="leaf")
        if path: # path is in handlers and handlers are not empty
            if include is None or "/".join(path) in include:
                return self.handlers[path].get_value(subpath or None)
        elif name in self.handlers:
            values=dictionary.Dictionary()
            subtree=self.handlers[name]
            for n in subtree.paths():
                if include is None or "/".join(n) in include:
                    values[n]=subtree[n].get_value()
            if values:
                return values
        raise KeyError("missing handler '{}'".format(name))
    get_all_values=get_value
    @gui_thread_method
    def set_value(self, name, value, include=None):
        """
        Set value under a given name.

        Automatically handles complex widgets and sub-names
        """
        name=name or ""
        path,subpath=self.handlers.get_max_prefix(name,kind="leaf")
        if path: # path is in handlers and handlers are not empty
            if include is None or "/".join(path) in include:
                return self.handlers[path].set_value(value,subpath or None)
        elif name in self.handlers:
            subtree=self.handlers[name]
            for n,v in dictionary.as_dictionary(value).iternodes(to_visit="all",topdown=True,include_path=True):
                if subtree.has_entry(n,kind="leaf"):
                    if (include is None) or ("/".join(n) in include):
                        subtree[n].set_value(v)
            return
        raise KeyError("missing handler '{}'".format(name))
    def set_all_values(self, value, root="", include=None):
        return self.set_value(root,value,include=include)

    @gui_thread_method
    def get_indicator(self, name=None, ind_name="__default__", include=None):
        """
        Get indicator value with a given name.

        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        """
        name=name or ""
        path,subpath=self.indicator_handlers.get_max_prefix(name,kind="leaf")
        if path: # path is in indicator_handlers and indicator_handlers are not empty
            if include is None or "/".join(path) in include:
                ind_set=self.indicator_handlers[path].ind
                if ind_name not in ind_set:
                    raise KeyError("missing indicator handler '{}' for with sub-name '{}'".format(name,ind_name))
                return ind_set[ind_name].get_value(subpath or None)
        elif name in self.indicator_handlers:
            values=dictionary.Dictionary()
            subtree=self.indicator_handlers[name]
            for n in subtree.paths():
                if (include is None) or ("/".join(n) in include):
                    ind_set=subtree[n].ind
                    if ind_name in ind_set:
                        values[n]=ind_set[ind_name].get_value()
            if values:
                return values
        raise KeyError("missing indicator handler '{}'".format(name))
    get_all_indicators=get_indicator
    @gui_thread_method
    def set_indicator(self, name, value, ind_name=None, include=None):
        """
        Set indicator value with a given name.

        `ind_name` can distinguish different sub-indicators with the same name, if the same value has multiple indicators.
        By default, set all sub-indicators to the given value.
        """
        name=name or ""
        path,subpath=self.indicator_handlers.get_max_prefix(name,kind="leaf")
        if path: # path is in indicator_handlers and indicator_handlers are not empty
            if include is None or "/".join(path) in include:
                ind_set=self.indicator_handlers[path].ind
                if ind_name is None:
                    for ind in ind_set.values():
                        ind.set_value(value,subpath or None)
                    return
                elif ind_name in ind_set:
                    return ind_set[ind_name].set_value(value,subpath or None)
                else:
                    raise KeyError("missing handler '{}' for indicator with sub-name '{}'".format(name,ind_name))
        elif name in self.indicator_handlers:
            subtree=self.indicator_handlers[name]
            for n,v in dictionary.as_dictionary(value).iternodes(to_visit="all",topdown=True,include_path=True):
                if subtree.has_entry(n,kind="leaf"):
                    if (include is None) or ("/".join(n) in include):
                        ind_set=subtree[n].ind
                        if ind_name is None:
                            for ind in ind_set.values():
                                ind.set_value(v)
                        elif ind_name in ind_set:
                            ind_set[ind_name].set_value(v)
            return
        raise KeyError("missing handler '{}'".format(name))
    def set_all_indicators(self, value, root="", ind_name=None, include=None):
        return self.set_indicator(root,value,ind_name=ind_name,include=include)
    @gui_thread_method
    def update_indicators(self, root="", include=None):
        """
        Update all indicators in a subtree with the given root (all values by default) to represent current values.
        
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
            
    def repr_value(self, name, value):
        """
        Get a textual representation of a value under a given name.

        Automatically handles complex widgets and sub-names.
        """
        path,subpath=self.handlers.get_max_prefix(name,kind="leaf")
        if path is None:
            raise KeyError("missing handler {}".format(name))
        return self.handlers[path].repr_value(value,subpath)
    def value_changed(self, name):
        """Get changed events for a value under a given name"""
        return self.handlers[name].value_changed()



def create_virtual_values(**kwargs):
    """
    Create a gui values set with all virtual values.

    ``kwargs`` define element names and default values.
    """
    values=GUIValues()
    for k,v in kwargs.items():
        values.add_virtual_element(k,v)