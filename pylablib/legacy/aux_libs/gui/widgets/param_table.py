from ....core.gui.qt.widgets import edit, label as widget_label
from ....core.gui.qt.thread import threadprop, controller
from ....core.gui.qt import values as values_module, utils
from ....core.utils import py3, dictionary

from PyQt5 import QtCore, QtWidgets

import collections

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class ParamTable(QtWidgets.QWidget):
    """
    GUI parameter table.
    
    Simplifies creating code-generated controls and displays table layouts.
    
    Has methods for adding various kinds of controls (labels, edit boxes, combo boxes, check boxes),
    automatically creates values table for easy settings/getting.
    By default supports 2-column (label-control) and 3-column (label-control-indicator) layout, depending on the parameters given to :meth:`setupUi`.

    Similar to :class:`.IndicatorValuesTable`, has three container-like accessor:
    ``.v`` for settings/getting values
    (i.e., ``self.get_value(name)`` is equivalent to ``self.v[name]``, and ``self.set_value(name, value)`` is equivalent to ``self.v[name]=value``),
    ``.i`` for settings/getting indicator values
    (i.e., ``self.get_indicator(name)`` is equivalent to ``self.i[name]``, and ``self.set_indicator(name, value)`` is equivalent to ``self.i[name]=value``),
    and ``.w`` for getting the underlying widget
    (i.e., ``self.get_widget(name)`` is equivalent to ``self.w[name]``)

    Like most widgets, requires calling :meth:`setupUi` to set up before usage.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None):
        super(ParamTable, self).__init__(parent)
        self.params={}
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)
        self.i=dictionary.ItemAccessor(self.get_indicator,self.set_indicator)
        self.w=dictionary.ItemAccessor(self.get_widget)

    def setupUi(self, name, add_indicator=False, display_table=None, display_table_root=None, gui_thread_safe=False):
        """
        Setup the table.

        Args:
            name (str): table widget name
            add_indicator (bool): if ``True``, add indicators for all added widgets by default.
            display_table (bool): as :class:`.IndicatorValuesTable` object used to access table values; by default, create one internally
            display_table_root (str): if not ``None``, specify root (i.e., path prefix) for values inside the table;
                if not specified, then there's no additional root for internal table (``display_table is None``),
                or it is equal to `name` if there is an external table  (``display_table is not None``)
            gui_thread_safe (bool): if ``True``, all value-access and indicator-access calls
                (``get/set_value``, ``get/set_all_values``, ``get/set_indicator``, and ``update_indicators``) are automatically called in the GUI thread.
        """
        self.name=name
        self.setObjectName(_fromUtf8(self.name))
        self.formLayout = QtWidgets.QGridLayout(self)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setContentsMargins(5,5,5,5)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.add_indicator=add_indicator
        self.change_focused_control=False
        if display_table is None:
            self.display_table=values_module.IndicatorValuesTable()
            self.display_table_root=""
        else:
            self.display_table=display_table
            self.display_table_root=display_table_root if display_table_root is not None else self.name
        self.gui_thread_safe=gui_thread_safe

    value_changed=QtCore.pyqtSignal("PyQt_PyObject","PyQt_PyObject")

    def _normalize_location(self, location, default=(None,0,1,1)):
        if not isinstance(location,(list,tuple)):
            location=(location,)
        location+=(None,)*(4-len(location))
        location=[d if l is None else l for (l,d) in zip(location,default)]
        row,col,rowspan,colspan=location
        row_cnt=self.formLayout.rowCount()
        row=row_cnt if row is None else (row%row_cnt)
        return row,col,rowspan,colspan
    ParamRow=collections.namedtuple("ParamRow",["widget","label","value_handler","indicator_handler"])
    def _add_widget(self, name, params):
        self.params[name]=params
        path=(self.display_table_root,name)
        self.display_table.add_handler(path,params.value_handler)
        if params.indicator_handler:
            self.display_table.add_indicator_handler(path,params.indicator_handler)
        changed_signal=params.value_handler.value_changed_signal()
        if changed_signal:
            changed_signal.connect(lambda value: self.value_changed.emit(name,value))
    def add_simple_widget(self, name, widget, label=None, value_handler=None, add_indicator=None, location=(None,0)):
        """
        Add a 'simple' (single-spaced, single-valued) widget to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            widget: widget to add
            label (str): if not ``None``, specifies label to put in front of the widget in the layout
            value_handler: value handler of the widget; by default, use auto-detected value handler (works for many simple built-in or custom widgets)
            add_indicator: if ``True``, add an indicator label in the third column and a corresponding indicator handler in the built-in values table;
                by default, use the default value supplied to :meth:`setupUi`
            location (tuple): tuple ``(row, column)`` specifying location of the widget (or widget label, if it is specified);
                by default, add to a new row in the end and into the first column
        
        Return the widget's value handler
        """
        if name in self.params:
            raise KeyError("widget {} already exists".format(name))
        row,col,rowspan,_=self._normalize_location(location)
        if label is not None:
            wlabel=QtWidgets.QLabel(self)
            wlabel.setObjectName(_fromUtf8("{}__label".format(name)))
            self.formLayout.addWidget(wlabel,row,col,rowspan,1)
            wlabel.setText(_translate(self.name,label,None))
        else:
            wlabel=None
        value_handler=value_handler or values_module.get_default_value_handler(widget)
        if add_indicator is None:
            add_indicator=self.add_indicator
        if add_indicator:
            windicator=QtWidgets.QLabel(self)
            windicator.setObjectName(_fromUtf8("{}__indicator".format(name)))
            self.formLayout.addWidget(windicator,row,col+2,rowspan,1)
            indicator_handler=values_module.WidgetLabelIndicatorHandler(windicator,widget=value_handler)
        else:
            indicator_handler=None
        if wlabel is None:
            self.formLayout.addWidget(widget,row,col,rowspan,2 if add_indicator else 3)
        else:
            self.formLayout.addWidget(widget,row,col+1,rowspan,1 if add_indicator else 2)
        self._add_widget(name,self.ParamRow(widget,wlabel,value_handler,indicator_handler))
        return value_handler

    def add_custom_widget(self, name, widget, value_handler=None, indicator_handler=None, location=(None,0,1,None)):
        """
        Add a 'custom' (multi-spaced, possibly complex-valued) widget to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            widget: widget to add
            value_handler: value handler of the widget; by default, use auto-detected value handler (works for many simple built-in or custom widgets)
            indicator_handler: indicator handler of the widget; by default, use auto-detected indciator handler
                (use ``set/get_indicator`` methods if present, or no indicator otherwises)
            location (tuple): tuple ``(row, column, rowspan, colspan)`` specifying location of the widget;
                by default, add to a new row in the end and into the first column, span one row and all table columns
        
        Return the widget's value handler
        """
        if name in self.params:
            raise KeyError("widget {} already exists".format(name))
        location=self._normalize_location(location,default=(None,0,1,3))
        self.formLayout.addWidget(widget,*location)
        value_handler=value_handler or values_module.get_default_value_handler(widget)
        indicator_handler=indicator_handler or values_module.get_default_indicator_handler(widget)
        self._add_widget(name,self.ParamRow(widget,None,value_handler,indicator_handler))
        return value_handler

    def add_virtual_element(self, name, value=None, add_indicator=None):
        """
        Add a virtual table element.

        Doesn't correspond to any actual widget, but behaves very similarly from the application point of view
        (its value can be set or read, it has on-change events, it can have indicator).
        """
        value_handler=values_module.VirtualValueHandler(value)
        if add_indicator is None:
            add_indicator=self.add_indicator
        indicator_handler=values_module.VirtualIndicatorHandler if add_indicator else None
        self._add_widget(name,self.ParamRow(None,None,value_handler,indicator_handler))
    def add_button(self, name, caption, checkable=False, value=False, label=None, add_indicator=None, location=(None,0)):
        """
        Add a button to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            caption (str): text on the button
            checkable (bool): determines whether the button is checkable (has on/off state) or simple press button
            value (bool): if checkable, specifies initial value

        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        widget=QtWidgets.QPushButton(self)
        widget.setText(_translate(self.name,caption,None))
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        widget.setCheckable(checkable)
        widget.setChecked(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location)
    def add_check_box(self, name, caption, value=False, label=None, add_indicator=None, location=(None,0)):
        """
        Add a checkbox to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            caption (str): text on the checkbox
            value (bool): specifies initial value
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        widget=QtWidgets.QCheckBox(self)
        widget.setText(_translate(self.name,caption,None))
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        widget.setChecked(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location)
    def add_text_label(self, name, value=None, label=None, location=(None,0)):
        """
        Add a text label to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        widget=QtWidgets.QLabel(self)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        if value is not None:
            widget.setText(str(value))
        return self.add_simple_widget(name,widget,label=label,add_indicator=False,location=location)
    def add_num_label(self, name, value=0, limiter=None, formatter=None, label=None, location=(None,0)):
        """
        Add a numerical label to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (float): specifies initial value
            limiter (tuple): tuple ``(upper_limit, lower_limit, action, value_type)`` specifying value limits;
                see :func:`.limit.as_limiter` for details
            formatter (tuple): either ``"int"`` (for integer values), or tuple specifying floating value format;
                see :func:`.format.as_formatter` for details
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        widget=widget_label.LVNumLabel(self,value=value,num_limit=limiter,num_format=formatter)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        return self.add_simple_widget(name,widget,label=label,add_indicator=False,location=location)
    def add_text_edit(self, name, value=None, label=None, add_indicator=None, location=(None,0)):
        """
        Add a text edit to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        widget=edit.LVTextEdit(self,value=value)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location)
    def add_num_edit(self, name, value=None, limiter=None, formatter=None, label=None, add_indicator=None, location=(None,0)):
        """
        Add a numerical edit to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            limiter (tuple): tuple ``(upper_limit, lower_limit, action, value_type)`` specifying value limits;
                see :func:`.limit.as_limiter` for details
            formatter (tuple): either ``"int"`` (for integer values), or tuple specifying floating value format;
                see :func:`.format.as_formatter` for details
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        widget=edit.LVNumEdit(self,value=value,num_limit=limiter,num_format=formatter)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location)
    def add_progress_bar(self, name, value=None, label=None):
        """
        Add a progress bar to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        widget=QtWidgets.QProgressBar(self)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        if value is not None:
            widget.setValue(value)
        return self.add_simple_widget(name,widget,label=label)
    def add_combo_box(self, name, value=None, options=None, label=None, add_indicator=None):
        """
        Add a combo box to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            options (list): list of string specifying box options
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        widget=QtWidgets.QComboBox(self)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        if options:
            widget.addItems(options)
            if value is not None:
                widget.setCurrentIndex(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator)

    def add_spacer(self, height, width=1, location=(None,0)):
        """Add a spacer with the given width and height"""
        spacer=QtWidgets.QSpacerItem(width,height,QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        location=self._normalize_location(location)
        self.formLayout.addItem(spacer,*location)
        return spacer
    def add_label(self, text, location=(None,0)):
        """Add a text label (only for decoration) with the given text"""
        label=QtWidgets.QLabel(self)
        label.setText(str(text))
        label.setAlignment(QtCore.Qt.AlignLeft)
        location=self._normalize_location(location)
        self.formLayout.addWidget(label,*location)
        return label
    def add_padding(self, prop=1):
        """Add a padding (expandable spacer) with the given proportion"""
        self.add_spacer(0)
        self.formLayout.setRowStretch(self.formLayout.rowCount(),prop)
    def insert_row(self, row):
        """Insert a new table row at the given location"""
        utils.insert_layout_row(self.formLayout,row)

    def lock(self, names=None, locked=True):
        """Lock (disable) or unlock (enable) widgets with the given names (by default, all widgets)"""
        if isinstance(names,py3.anystring):
            names=[names]
        if names is None:
            names=self.params.keys()
        for name in names:
            widget=self.params[name].widget
            if widget is not None:
                widget.setEnabled(not locked)

    @controller.gui_thread_method
    def get_value(self, name):
        """Get value of a widget with the given name"""
        return self.display_table.get_value((self.display_table_root,name))
    @controller.gui_thread_method
    def set_value(self, name, value):
        """Set value of a widget with the given name"""
        par=self.params[name]
        if self.change_focused_control or par.widget is None or not par.widget.hasFocus():
            return self.display_table.set_value((self.display_table_root,name),value)
    @controller.gui_thread_method
    def get_all_values(self):
        """Get values of all widgets in the table"""
        return self.display_table.get_all_values(root=self.display_table_root,include=self.params)
    @controller.gui_thread_method
    def set_all_values(self, values):
        """Set values of all widgets in the table"""
        return self.display_table.set_all_values(values,root=self.display_table_root,include=self.params)

    def get_handler(self, name):
        """Get value handler of a widget with the given name"""
        return self.params[name].value_handler
    def get_widget(self, name):
        """Get a widget with the given name"""
        return self.params[name].widget
    def changed_event(self, name):
        """Get a value-changed signal for a widget with the given name"""
        return self.params[name].value_handler.value_changed_signal()

    @controller.gui_thread_method
    def get_indicator(self, name):
        """Get indicator value for a widget with the given name"""
        return self.display_table.get_indicator((self.display_table_root,name))
    @controller.gui_thread_method
    def set_indicator(self, name, value):
        """Set indicator value for a widget with the given name"""
        return self.display_table.set_indicator((self.display_table_root,name),value)
    @controller.gui_thread_method
    def get_all_indicators(self):
        """Get all indicator values"""
        return self.display_table.get_all_indicators(root=self.display_table_root)
    @controller.gui_thread_method
    def update_indicators(self):
        """Update all indicators (set their value """
        return self.display_table.update_indicators(root=self.display_table_root,include=self.params)

    def clear(self, disconnect=False):
        """
        Clear the table (remove all widgets)
        
        If ``disconnect==True``, also disconnect all slots connected to the ``value_changed`` signal.
        """
        if self.params:
            if disconnect:
                try:
                    self.value_changed.disconnect()
                except TypeError: # no signals connected
                    pass
            for name in self.params:
                path=(self.display_table_root,name)
                self.display_table.remove_handler(path)
                self.display_table.remove_indicator_handler(path)
            self.params={}
            utils.clean_layout(self.formLayout,delete_layout=True)
            self.formLayout = QtWidgets.QGridLayout(self)
            self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            self.formLayout.setContentsMargins(5,5,5,5)
            self.formLayout.setObjectName(_fromUtf8("formLayout"))

    
    def __getitem__(self, name):
        return self.get_handler(name)
    def __contains__(self, name):
        return name in self.params

TFixedParamTable=collections.namedtuple("FixedParamTable",["v","i"])
def FixedParamTable(v=None,i=None):
    return TFixedParamTable(v=v or {}, i=i or {})


class StatusTable(ParamTable):
    """
    Expansion of :class:`ParamTable` which adds status lines, which automatically subscribe to signals and update values.
    """
    def add_status_line(self, name, label=None, srcs=None, tags=None, filt=None, make_status=None):
        """
        Add a status line to the table:

        Args:
            name (str): widget name (used to reference its value in the values table)
            label (str): if not ``None``, specifies label to put in front of the status line
            srcs (list): status signal sources
            tags (list): status signal tags
            filt (list): filter function for the signals
            make_status: if not ``None``, specifies a function which takes 3 arguments (signal source, tag, and value) and generates a status line text.
        """
        self.add_text_label(name,label=label)
        def update_text(src, tag, value):
            if make_status is not None:
                text=make_status(src,tag,value)
            else:
                text=value
            self.v[name]=text
        threadprop.current_controller().subscribe(update_text,srcs=srcs,dsts="any",tags=tags,filt=filt,limit_queue=10)