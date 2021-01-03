from . import edit, label as widget_label
from ...thread import threadprop, controller
from .. import value_handling as value_handling, utils
from ...utils import py3, dictionary

from PyQt5 import QtCore, QtWidgets

import collections

try:
    _fromUtf8=QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding=QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context,text,disambig,_encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context,text,disambig)


class ParamTable(QtWidgets.QWidget):
    """
    GUI parameter table.
    
    Simplifies creating code-generated controls and displays table layouts.
    
    Has methods for adding various kinds of controls (labels, edit boxes, combo boxes, check boxes),
    automatically creates values table for easy settings/getting.
    By default supports 2-column (label-control) and 3-column (label-control-indicator) layout, depending on the parameters given to :meth:`setupUi`.

    Similar to :class:`.ValuesTable`, has three container-like accessor:
    ``.h`` for getting the value handler
    (i.e., ``self.get_handler(name)`` is equivalent to ``self.h[name]``),
    ``.w`` for getting the underlying widget
    (i.e., ``self.get_widget(name)`` is equivalent to ``self.w[name]``),
    ``.v`` for settings/getting values
    (i.e., ``self.get_value(name)`` is equivalent to ``self.v[name]``, and ``self.set_value(name, value)`` is equivalent to ``self.v[name]=value``),
    ``.i`` for settings/getting indicator values
    (i.e., ``self.get_indicator(name)`` is equivalent to ``self.i[name]``, and ``self.set_indicator(name, value)`` is equivalent to ``self.i[name]=value``)

    Like most widgets, requires calling :meth:`setupUi` to set up before usage.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None):
        super(ParamTable, self).__init__(parent)
        self.params={}
        self.h=dictionary.ItemAccessor(self.get_handler)
        self.w=dictionary.ItemAccessor(self.get_widget)
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)
        self.i=dictionary.ItemAccessor(self.get_indicator,self.set_indicator)
    def setupUi(self, name, add_indicator=True, values_table=None, values_table_root=None, gui_thread_safe=False, cache_values=False, change_focused_control=False):
        """
        Setup the table.

        Args:
            name (str): table widget name
            add_indicator (bool): if ``True``, add indicators for all added widgets by default.
            values_table (bool): as :class:`.ValuesTable` object used to access table values; by default, create one internally
            values_table_root (str): if not ``None``, specify root (i.e., path prefix) for values inside the table;
                if not specified, then there's no additional root for internal table (``values_table is None``),
                or it is equal to `name` if there is an external table  (``values_table is not None``)
            gui_thread_safe (bool): if ``True``, all value-access and indicator-access calls
                (``get/set_value``, ``get/set_all_values``, ``get/set_indicator``, and ``update_indicators``) are automatically called in the GUI thread.
            cache_values (bool): if ``True`` or ``"update_one"``, store a dictionary with all the current values and update it every time a GUI value is changed;
                provides a thread-safe way to check current parameters without lag
                (unlike :meth:`get_all_values` with ``gui_thread_safe==True``, which re-routes call to a GUI thread and may cause up to 50ms delay)
                can also be set to ``"update_all"``, in which case change of any value will cause value update of all variables;
                otherwise, change of a value will only cause update of that same value (might potentially miss some value updates for custom controls).
            change_focused_control (bool): if ``False`` and :meth:`set_value` method is called while the widget has user focus, ignore the value;
                note that :meth:`set_all_values` will still set the widget value.
        """
        self.name=name
        self.setObjectName(_fromUtf8(self.name))
        self.formLayout=QtWidgets.QGridLayout(self)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setContentsMargins(5,5,5,5)
        self.formLayout.setObjectName(_fromUtf8(self.name+"_formLayout"))
        self.add_indicator=add_indicator
        if values_table is None:
            self.values_table=value_handling.ValuesTable()
            self.values_table_root=""
        else:
            self.values_table=values_table
            self.values_table_root=values_table_root if values_table_root is not None else self.name
        self.gui_thread_safe=gui_thread_safe
        self.change_focused_control=change_focused_control
        self.cache_values=cache_values
        self.current_values=dictionary.Dictionary()

    value_changed=QtCore.pyqtSignal(object,object)
    @controller.exsafeSlot()
    def _update_cache_values(self, name=None, value=None):
        if self.cache_values:
            if name is None or self.cache_values=="update_all":
                self.current_values=self.get_all_values()
            else:
                self.current_values[name]=self.get_value(name)

    def _normalize_location(self, location, default=(None,0,1,1)):
        if location=="skip":
            return "skip"
        if not isinstance(location,(list,tuple)):
            location=(location,)
        location+=(None,)*(4-len(location))
        location=[d if l is None else l for (l,d) in zip(location,default)]
        row,col,rowspan,colspan=location
        row_cnt=self.formLayout.rowCount()
        row=row_cnt if row is None else (row%row_cnt)
        return row,col,rowspan,colspan
    ParamRow=collections.namedtuple("ParamRow",["widget","label","indicator","value_handler","indicator_handler"])
    def _add_widget(self, name, params, add_change_event=True):
        self.params[name]=params
        path=(self.values_table_root,name)
        self.values_table.add_handler(path,params.value_handler)
        if params.indicator_handler:
            self.values_table.add_indicator_handler(path,params.indicator_handler)
        if add_change_event:
            params.value_handler.connect_value_changed_handler(lambda value: self.value_changed.emit(name,value),only_signal=True)
        if self.cache_values:
            params.value_handler.connect_value_changed_handler(lambda value: self._update_cache_values(name,value),only_signal=False)
        self._update_cache_values()
    def add_simple_widget(self, name, widget, label=None, value_handler=None, add_indicator=None, location=(None,0), add_change_event=True):
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
                can also be a string ``"skip"``, which means that the widget is added to some other location manually later
                (this option only works if ``label=None``, and doesn't add any indicator)
            add_change_event (bool): if ``True``, changing of the widget's value emits the table's ``value_changed`` event
        
        Return the widget's value handler
        """
        if name in self.params:
            raise KeyError("widget {} already exists".format(name))
        location=self._normalize_location(location,default=(None,0,1,None))
        if location!="skip":
            row,col,rowspan,colspan=location
        if label is not None:
            wlabel=QtWidgets.QLabel(self)
            wlabel.setObjectName(_fromUtf8("{}__label".format(name)))
            self.formLayout.addWidget(wlabel,row,col,rowspan,1)
            wlabel.setText(_translate(self.name,label,None))
        else:
            wlabel=None
        value_handler=value_handler or value_handling.create_value_handler(widget)
        if add_indicator is None:
            add_indicator=self.add_indicator and (location!="skip")
        if add_indicator:
            windicator=QtWidgets.QLabel(self)
            windicator.setObjectName(_fromUtf8("{}__indicator".format(name)))
            self.formLayout.addWidget(windicator,row,col+2,rowspan,1)
            indicator_handler=value_handling.LabelIndicatorHandler(windicator,formatter=value_handler)
        else:
            windicator=None
            indicator_handler=None
        if wlabel is None:
            self.formLayout.addWidget(widget,row,col,rowspan,colspan or (2 if add_indicator else 3))
        elif location!="skip":
            self.formLayout.addWidget(widget,row,col+1,rowspan,colspan or (1 if add_indicator else 2))
        self._add_widget(name,self.ParamRow(widget,wlabel,windicator,value_handler,indicator_handler),add_change_event=add_change_event)
        return value_handler

    def add_custom_widget(self, name, widget, value_handler=None, indicator_handler=None, location=(None,0,1,None), add_change_event=True):
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
                can also be a string ``"skip"``, which means that the widget is added to some other location manually later
            add_change_event (bool): if ``True``, changing of the widget's value emits the table's ``value_changed`` event
        
        Return the widget's value handler
        """
        if name in self.params:
            raise KeyError("widget {} already exists".format(name))
        location=self._normalize_location(location,default=(None,0,1,3))
        if location!="skip":
            self.formLayout.addWidget(widget,*location)
        value_handler=value_handler or value_handling.create_value_handler(widget)
        indicator_handler=indicator_handler or value_handling.create_indicator_handler(widget)
        self._add_widget(name,self.ParamRow(widget,None,None,value_handler,indicator_handler),add_change_event=add_change_event)
        return value_handler

    def add_virtual_element(self, name, value=None, add_indicator=None):
        """
        Add a virtual table element.

        Doesn't correspond to any actual widget, but behaves very similarly from the application point of view
        (its value can be set or read, it has on-change events, it can have indicator).
        """
        value_handler=value_handling.VirtualValueHandler(value)
        if add_indicator is None:
            add_indicator=self.add_indicator
        indicator_handler=value_handling.VirtualIndicatorHandler if add_indicator else None
        self._add_widget(name,self.ParamRow(None,None,None,value_handler,indicator_handler))
    def add_button(self, name, caption, checkable=False, value=False, label=None, add_indicator=None, location=(None,0), add_change_event=True, virtual=False):
        """
        Add a button to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            caption (str): text on the button
            checkable (bool): determines whether the button is checkable (has on/off state) or simple press button
            value (bool): if checkable, specifies initial value
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead

        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=QtWidgets.QPushButton(self)
        widget.setText(_translate(self.name,caption,None))
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        widget.setCheckable(checkable)
        widget.setChecked(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,add_change_event=add_change_event)
    def add_check_box(self, name, caption, value=False, label=None, add_indicator=None, location=(None,0), add_change_event=True, virtual=False):
        """
        Add a checkbox to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            caption (str): text on the checkbox
            value (bool): specifies initial value
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=QtWidgets.QCheckBox(self)
        widget.setText(_translate(self.name,caption,None))
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        widget.setChecked(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,add_change_event=add_change_event)
    def add_text_label(self, name, value=None, label=None, location=(None,0), add_change_event=False, virtual=False):
        """
        Add a text label to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value)
        widget=widget_label.LVTextLabel(self,value=value)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        return self.add_simple_widget(name,widget,label=label,add_indicator=False,location=location,add_change_event=add_change_event)
    def add_num_label(self, name, value=0, limiter=None, formatter=None, label=None, location=(None,0), add_change_event=False, virtual=False):
        """
        Add a numerical label to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (float): specifies initial value
            limiter (tuple): tuple ``(upper_limit, lower_limit, action, value_type)`` specifying value limits;
                see :func:`.limit.as_limiter` for details
            formatter (tuple): either ``"int"`` (for integer values), or tuple specifying floating value format;
                see :func:`.format.as_formatter` for details
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value)
        widget=widget_label.LVNumLabel(self,value=value,limiter=limiter,formatter=formatter)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        return self.add_simple_widget(name,widget,label=label,add_indicator=False,location=location,add_change_event=add_change_event)
    def add_text_edit(self, name, value=None, label=None, add_indicator=None, location=(None,0), add_change_event=True, virtual=False):
        """
        Add a text edit to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=edit.LVTextEdit(self,value=value)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,add_change_event=add_change_event)
    def add_num_edit(self, name, value=None, limiter=None, formatter=None, custom_steps=None, label=None, add_indicator=None, location=(None,0), add_change_event=True, virtual=False):
        """
        Add a numerical edit to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            limiter (tuple): tuple ``(upper_limit, lower_limit, action, value_type)`` specifying value limits;
                see :func:`.LVNumEdit.set_limiter` for details
            formatter (tuple): either ``"int"`` (for integer values), or tuple specifying floating value format;
                see :func:`.LVNumEdit.set_formatter` for details
            custom_steps: if not ``None``, can specify custom fixed value steps when up/down keys are pressed with a modifier key (Control, Alt, or Shift)
                specifies a dictionary ``{'ctrl':ctrl_step, 'alt':alt_step, 'shift':shift_step}`` with the corresponding steps (missing elements mean that the modifier key is ignored)
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=edit.LVNumEdit(self,value=value,limiter=limiter,formatter=formatter,custom_steps=custom_steps)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,add_change_event=add_change_event)
    def add_progress_bar(self, name, value=None, label=None, add_change_event=True, virtual=False):
        """
        Add a progress bar to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value)
        widget=QtWidgets.QProgressBar(self)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        if value is not None:
            widget.setValue(value)
        return self.add_simple_widget(name,widget,label=label,add_change_event=add_change_event)
    def add_combo_box(self, name, value=None, options=None, label=None, add_indicator=None, add_change_event=True, virtual=False):
        """
        Add a combo box to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            options (list): list of string specifying box options
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=QtWidgets.QComboBox(self)
        widget.setObjectName(_fromUtf8(self.name+"_"+name))
        if options:
            widget.addItems(options)
            if value is not None:
                widget.setCurrentIndex(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,add_change_event=add_change_event)

    def add_spacer(self, height, width=1, location=(None,0)):
        """Add a spacer with the given width and height"""
        spacer=QtWidgets.QSpacerItem(width,height,QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        location=self._normalize_location(location)
        self.formLayout.addItem(spacer,*location)
        return spacer
    def add_padding(self, prop=1):
        """Add a padding (expandable spacer) with the given proportion"""
        self.add_spacer(0)
        self.formLayout.setRowStretch(self.formLayout.rowCount(),prop)
    def add_decoration_label(self, text, location=(None,0)):
        """Add a text label (only for decoration) with the given text"""
        label=QtWidgets.QLabel(self)
        label.setText(str(text))
        label.setAlignment(QtCore.Qt.AlignLeft)
        location=self._normalize_location(location)
        self.formLayout.addWidget(label,*location)
        return label
    def insert_row(self, row):
        """Insert a new table row at the given location"""
        utils.insert_layout_row(self.formLayout,row%(self.formLayout.rowCount() or 1))

    def set_enabled(self, names=None, enabled=True, include_indicator=True, include_label=True):
        """Enable or disable widgets with the given names (by default, all widgets)"""
        if isinstance(names,py3.anystring):
            names=[names]
        if names is None:
            names=self.params.keys()
        for name in names:
            par=self.params[name]
            if par.widget is not None:
                par.widget.setEnabled(enabled)
            if include_label and par.label is not None:
                par.label.setEnabled(enabled)
            if include_indicator and par.indicator is not None:
                par.indicator.setEnabled(enabled)
    def set_visible(self, names=None, visible=True, include_indicator=True, include_label=True):
        """Show or hide widgets with the given names (by default, all widgets)"""
        if isinstance(names,py3.anystring):
            names=[names]
        if names is None:
            names=self.params.keys()
        for name in names:
            par=self.params[name]
            if par.widget is not None:
                par.widget.setVisible(visible)
            if include_label and par.label is not None:
                par.label.setVisible(visible)
            if include_indicator and par.indicator is not None:
                par.indicator.setVisible(visible)

    @controller.gui_thread_method
    def get_value(self, name):
        """Get value of a widget with the given name"""
        return self.values_table.get_value((self.values_table_root,name))
    @controller.gui_thread_method
    def set_value(self, name, value, force=False):
        """
        Set value of a widget with the given name
        
        If ``force==True``, force widget value (e.g., ignoring restriction on not changing values of focused widgets)
        """
        par=self.params[name]
        if force or par.value_handler.is_set_allowed(allow_focus=self.change_focused_control):
            return self.values_table.set_value((self.values_table_root,name),value)
    @controller.gui_thread_method
    def get_all_values(self):
        """Get values of all widgets in the table"""
        return self.values_table.get_all_values(root=self.values_table_root,include=self.params)
    @controller.gui_thread_method
    def set_all_values(self, values):
        """Set values of all widgets in the table"""
        return self.values_table.set_all_values(values,root=self.values_table_root,include=self.params)

    def get_handler(self, name):
        """Get value handler of a widget with the given name"""
        return self.params[name].value_handler
    def get_widget(self, name):
        """Get a widget with the given name"""
        return self.params[name].widget
    def widget_value_changed(self, name):
        """Get a value-changed signal for a widget with the given name"""
        return self.params[name].value_handler.value_changed()

    @controller.gui_thread_method
    def get_indicator(self, name):
        """Get indicator value for a widget with the given name"""
        return self.values_table.get_indicator((self.values_table_root,name))
    @controller.gui_thread_method
    def set_indicator(self, name, value):
        """Set indicator value for a widget with the given name"""
        return self.values_table.set_indicator((self.values_table_root,name),value)
    @controller.gui_thread_method
    def get_all_indicators(self):
        """Get all indicator values"""
        return self.values_table.get_all_indicators(root=self.values_table_root)
    @controller.gui_thread_method
    def update_indicators(self):
        """Update all indicators (set their value """
        return self.values_table.update_indicators(root=self.values_table_root,include=self.params)

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
                path=(self.values_table_root,name)
                self.values_table.remove_handler(path)
                self.values_table.remove_indicator_handler(path)
            self.params={}
            utils.clean_layout(self.formLayout,delete_layout=True)
            self.formLayout = QtWidgets.QGridLayout(self)
            self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            self.formLayout.setContentsMargins(5,5,5,5)
            self.formLayout.setObjectName(_fromUtf8("formLayout"))
            self._update_cache_values()

    def __contains__(self, name):
        return name in self.params



class StatusTable(ParamTable):
    """
    Expansion of :class:`ParamTable` which adds status lines, which automatically subscribe to signals and update values.
    """
    def add_status_line(self, name, label=None, srcs=None, tags=None, filt=None, fmt=None):
        """
        Add a status line to the table:

        Args:
            name (str): widget name (used to reference its value in the values table)
            label (str): if not ``None``, specifies label to put in front of the status line
            srcs (list): status signal sources
            tags (list): status signal tags
            filt (list): filter function for the signals
            fmt: if not ``None``, specifies a function which takes 3 arguments (signal source, tag, and value) and generates a status line text.
        """
        self.add_text_label(name,label=label)
        def update_text(src, tag, value):
            if fmt is not None:
                text=fmt(src,tag,value)
            else:
                text=value
            self.v[name]=text
        threadprop.current_controller().subscribe(update_text,srcs=srcs,dsts="any",tags=tags,filt=filt,limit_queue=10)