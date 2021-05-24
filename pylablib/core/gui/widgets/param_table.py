from . import edit, label as widget_label, combo_box, button as widget_button
from ...thread import threadprop, controller
from .. import value_handling as value_handling, utils
from ...utils import py3, dictionary

from .. import QtCore, QtWidgets, Signal

import collections


class ParamTable(QtWidgets.QWidget):
    """
    GUI parameter table.
    
    Simplifies creating code-generated controls and displays table layouts.
    
    Has methods for adding various kinds of controls (labels, edit boxes, combo boxes, check boxes),
    automatically creates values table for easy settings/getting.
    By default supports 2-column (label-control) and 3-column (label-control-indicator) layout, depending on the parameters given to :meth:`setupUi`.

    Similar to :class:`.GUIValues`, has three container-like accessor:
    ``.h`` for getting the value handler
    (i.e., ``self.get_handler(name)`` is equivalent to ``self.h[name]``),
    ``.w`` for getting the underlying widget
    (i.e., ``self.get_widget(name)`` is equivalent to ``self.w[name]``),
    ``.v`` for settings/getting values
    (i.e., ``self.get_value(name)`` is equivalent to ``self.v[name]``, and ``self.set_value(name, value)`` is equivalent to ``self.v[name]=value``),
    ``.i`` for settings/getting indicator values
    (i.e., ``self.get_indicator(name)`` is equivalent to ``self.i[name]``, and ``self.set_indicator(name, value)`` is equivalent to ``self.i[name]=value``)
    ``.vs`` for getting the value changed Qt signal
    (i.e., ``self.get_value_changed_signal(name)`` is equivalent to ``self.s[name]``),

    Like most widgets, requires calling :meth:`setupUi` to set up before usage.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.params={}
        self.h=dictionary.ItemAccessor(self.get_handler)
        self.w=dictionary.ItemAccessor(self.get_widget)
        self.v=dictionary.ItemAccessor(self.get_value,self.set_value)
        self.i=dictionary.ItemAccessor(self.get_indicator,self.set_indicator)
        self.vs=dictionary.ItemAccessor(self.get_value_changed_signal)
    def setupUi(self, name, add_indicator=True, gui_values=None, gui_values_root=None, gui_thread_safe=False, cache_values=False, change_focused_control=False):
        """
        Setup the table.

        Args:
            name (str): table widget name
            add_indicator (bool): if ``True``, add indicators for all added widgets by default.
            gui_values (bool): as :class:`.GUIValues` object used to access table values; by default, create one internally
            gui_values_root (str): if not ``None``, specify root (i.e., path prefix) for values inside the table;
                if not specified, then there's no additional root for internal table (``gui_values is None``),
                or it is equal to `name` if there is an external table  (``gui_values is not None``)
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
        self.setObjectName(self.name)
        self.formLayout=QtWidgets.QGridLayout(self)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setContentsMargins(5,5,5,5)
        self.formLayout.setSpacing(5)
        self.formLayout.setObjectName(self.name+"_formLayout")
        self._sublayouts={}
        self.add_indicator=add_indicator
        if gui_values is None:
            self.gui_values=value_handling.GUIValues()
            self.gui_values_root=""
        else:
            self.gui_values=gui_values
            self.gui_values_root=gui_values_root if gui_values_root is not None else self.name
        self.gui_thread_safe=gui_thread_safe
        self.change_focused_control=change_focused_control
        self.cache_values=cache_values
        self.current_values=dictionary.Dictionary()

    value_changed=Signal(object,object)
    @controller.exsafeSlot()
    def _update_cache_values(self, name=None, value=None):  # pylint: disable=unused-argument
        if self.cache_values:
            if name is None or self.cache_values=="update_all":
                self.current_values=self.get_all_values()
            else:
                self.current_values[name]=self.get_value(name)

    def _normalize_location(self, location, default=("next",0,1,1)):
        if location=="skip":
            return "skip"
        if not isinstance(location,(list,tuple)):
            location=(location,)
        if isinstance(location[0],py3.textstring) and location[0]!="next":
            lname,location=location[0],location[1:]
            layout,lkind=self._sublayouts[lname]
        else:
            lname=None
            layout,lkind=self.formLayout,"grid"
        location+=(None,)*(4-len(location))
        location=[d if l is None else l for (l,d) in zip(location,default)]
        row,col,rowspan,colspan=location
        if lkind=="grid":
            row_cnt,col_cnt=layout.rowCount(),layout.columnCount()
        elif lkind=="vbox":
            col,colspan,rowspan=0,1,1
            row_cnt,col_cnt=layout.count(),1
        else:
            if location[1:]==(None,None,None):
                row,col,rowspan,colspan=0,location[0],1,1
            row,colspan,rowspan=0,1,1
            row_cnt,col_cnt=1,layout.count()
        row=row_cnt if row=="next" else (row%row_cnt if row<0 else row)
        if rowspan=="end":
            rowspan=max(row_cnt-row,1)
        col=col_cnt if col=="next" else (col%col_cnt if col<0 else col)
        if colspan=="end":
            colspan=max(col_cnt-col,1)
        return lname,(row,col,rowspan,colspan)
    def _insert_layout_element(self, lname, element, location, kind="widget"):
        if lname is None:
            layout,lkind=self.formLayout,"grid"
        else:
            layout,lkind=self._sublayouts[lname]
        if lkind=="grid":
            if kind=="widget":
                layout.addWidget(element,*location)
            elif kind=="item":
                layout.addItem(element,*location)
            elif kind=="layout":
                layout.addLayout(element,*location)
            else:
                raise ValueError("unrecognized element kind: {}".format(kind))
        else:
            idx=location[0] if lkind=="vbox" else location[1]
            if lkind=="vbox" and location[0]!=0:
                raise ValueError("can't space widgets vertically in a vbox environment")
            if kind=="widget":
                layout.insertWidget(idx,element)
            elif kind=="item":
                layout.insertItem(idx,element)
            elif kind=="layout":
                layout.insertLayout(idx,element)
            else:
                raise ValueError("unrecognized element kind: {}".format(kind))
    def add_sublayout(self, name, kind="grid", location=("next",0,1,"end")):
        """
        Add a sublayout to the given location.

        `name` specifies the sublayout name, which can be used to refer to it in specifying locations later.
        `kind` can be ``"grid"``, ``"vbox"`` (vertical single-column box), or ``"hbox"`` (horizontal single-row box).
        """
        if name in self._sublayouts:
            raise ValueError("sublayout {} already exists".format(name))
        if kind=="grid":
            layout=QtWidgets.QGridLayout(self)
        elif kind=="vbox":
            layout=QtWidgets.QVBoxLayout(self)
        elif kind=="hbox":
            layout=QtWidgets.QHBoxLayout(self)
        else:
            raise ValueError("unrecognized layout kind: {}".format(kind))
        lname,location=self._normalize_location(location)
        self._insert_layout_element(lname,layout,location,kind="layout")
        self._sublayouts[name]=(layout,kind)

    ParamRow=collections.namedtuple("ParamRow",["widget","label","indicator","value_handler","indicator_handler"])
    def _add_widget(self, name, params, add_change_event=True):
        self.params[name]=params
        path=(self.gui_values_root,name)
        self.gui_values.add_handler(path,params.value_handler)
        if params.indicator_handler:
            self.gui_values.add_indicator_handler(path,params.indicator_handler)
        if add_change_event:
            params.value_handler.connect_value_changed_handler(lambda value: self.value_changed.emit(name,value),only_signal=True)
        if self.cache_values:
            params.value_handler.connect_value_changed_handler(lambda value: self._update_cache_values(name,value),only_signal=False)
        self._update_cache_values()
    def add_simple_widget(self, name, widget, label=None, value_handler=None, add_indicator=None, location="next", tooltip=None, add_change_event=True):
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
            tooltip: widget tooltip (mouseover text)
            add_change_event (bool): if ``True``, changing of the widget's value emits the table's ``value_changed`` event
        
        Return the widget's value handler
        """
        if name in self.params:
            raise KeyError("widget {} already exists".format(name))
        if add_indicator is None:
            add_indicator=self.add_indicator
        lname,location=self._normalize_location(location,default=("next",0,1,3 if add_indicator else 2))
        if location!="skip":
            row,col,rowspan,colspan=location
            labelspan=1 if label is not None else 0
            indspan=1 if add_indicator else 0
            if colspan<indspan+labelspan+1:
                raise ValueError("column span should be at least {} to accommodate the widget, the label, and the indicator".format(indspan+labelspan+1))
        else:
            if label is not None:
                raise ValueError("label can not be combined with 'skip' location")
            add_indicator=False
        if label is not None:
            wlabel=QtWidgets.QLabel(self)
            wlabel.setObjectName("{}__label".format(name))
            self._insert_layout_element(lname,wlabel,(row,col,rowspan,1))
            wlabel.setText(label)
        else:
            wlabel=None
        value_handler=value_handler or value_handling.create_value_handler(widget)
        if add_indicator:
            windicator=QtWidgets.QLabel(self)
            windicator.setObjectName("{}__indicator".format(name))
            self._insert_layout_element(lname,windicator,(row,col+colspan-1,rowspan,1))
            indicator_handler=value_handling.LabelIndicatorHandler(windicator,formatter=value_handler)
        else:
            windicator=None
            indicator_handler=None
        if location!="skip":
            self._insert_layout_element(lname,widget,(row,col+labelspan,rowspan,colspan-labelspan-indspan))
        if tooltip is not None:
            if wlabel is not None:
                wlabel.setToolTip(tooltip)
            else:
                widget.setToolTip(tooltip)
        self._add_widget(name,self.ParamRow(widget,wlabel,windicator,value_handler,indicator_handler),add_change_event=add_change_event)
        return value_handler

    def add_custom_widget(self, name, widget, value_handler=None, indicator_handler=None, location="next", tooltip=None, add_change_event=True):
        """
        Add a 'custom' (multi-spaced, possibly complex-valued) widget to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            widget: widget to add
            value_handler: value handler of the widget; by default, use auto-detected value handler (works for many simple built-in or custom widgets)
            indicator_handler: indicator handler of the widget; by default, use auto-detected indicator handler
                (use ``set/get_indicator`` methods if present, or no indicator otherwise)
            location (tuple): tuple ``(row, column, rowspan, colspan)`` specifying location of the widget;
                by default, add to a new row in the end and into the first column, span one row and all table columns
                can also be a string ``"skip"``, which means that the widget is added to some other location manually later
            add_change_event (bool): if ``True``, changing of the widget's value emits the table's ``value_changed`` event
        
        Return the widget's value handler
        """
        if name in self.params:
            raise KeyError("widget {} already exists".format(name))
        lname,location=self._normalize_location(location,default=("next",0,1,3))
        if location!="skip":
            self._insert_layout_element(lname,widget,location)
        value_handler=value_handler or value_handling.create_value_handler(widget)
        indicator_handler=indicator_handler or value_handling.create_indicator_handler(widget)
        if tooltip is not None:
            widget.setToolTip(tooltip)
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
    def add_button(self, name, caption, label=None, add_indicator=None, location="next", tooltip=None, add_change_event=True, virtual=False):
        """
        Add a button to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            caption (str): text on the button
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead

        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,add_indicator=add_indicator)
        widget=QtWidgets.QPushButton(self)
        widget.setText(caption)
        widget.setObjectName(self.name+"_"+name)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_toggle_button(self, name, caption, value=False, label=None, add_indicator=None, location="next", tooltip=None, add_change_event=True, virtual=False):
        """
        Add a toggle button to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            caption (str or list): text on the button; can be a single string, or a list of two strings which specifies the caption for off and on states
            value (bool): specifies initial value
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead

        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=widget_button.ToggleButton(self)
        if isinstance(caption,(tuple,list)):
            widget.set_value_labels([c for c in caption])
        else:
            widget.setText(caption)
        widget.setObjectName(self.name+"_"+name)
        widget.set_value(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_check_box(self, name, caption, value=False, label=None, add_indicator=None, location="next", tooltip=None, add_change_event=True, virtual=False):
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
        widget.setText(caption)
        widget.setObjectName(self.name+"_"+name)
        widget.setChecked(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_text_label(self, name, value=None, label=None, location="next", tooltip=None, add_change_event=False, virtual=False):
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
        widget=widget_label.TextLabel(self,value=value)
        widget.setObjectName(self.name+"_"+name)
        return self.add_simple_widget(name,widget,label=label,add_indicator=False,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_num_label(self, name, value=0, limiter=None, formatter=None, label=None, tooltip=None, location="next", add_change_event=False, virtual=False):
        """
        Add a numerical label to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (float): specifies initial value
            limiter (tuple): tuple ``(upper_limit, lower_limit, action, value_type)`` specifying value limits;
                see :func:`.limiter.as_limiter` for details
            formatter (tuple): either ``"int"`` (for integer values), or tuple specifying floating value format;
                see :func:`.formatter.as_formatter` for details
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value)
        widget=widget_label.NumLabel(self,value=value,limiter=limiter,formatter=formatter)
        widget.setObjectName(self.name+"_"+name)
        return self.add_simple_widget(name,widget,label=label,add_indicator=False,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_text_edit(self, name, value=None, label=None, add_indicator=None, location="next", tooltip=None, add_change_event=True, virtual=False):
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
        widget=edit.TextEdit(self,value=value)
        widget.setObjectName(self.name+"_"+name)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_num_edit(self, name, value=None, limiter=None, formatter=None, custom_steps=None, label=None, add_indicator=None, location="next", tooltip=None, add_change_event=True, virtual=False):
        """
        Add a numerical edit to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            limiter (tuple): tuple ``(upper_limit, lower_limit, action, value_type)`` specifying value limits;
                see :meth:`.NumEdit.set_limiter` for details
            formatter (tuple): either ``"int"`` (for integer values), or tuple specifying floating value format;
                see :meth:`.NumEdit.set_formatter` for details
            custom_steps: if not ``None``, can specify custom fixed value steps when up/down keys are pressed with a modifier key (Control, Alt, or Shift)
                specifies a dictionary ``{'ctrl':ctrl_step, 'alt':alt_step, 'shift':shift_step}`` with the corresponding steps (missing elements mean that the modifier key is ignored)
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=edit.NumEdit(self,value=value,limiter=limiter,formatter=formatter,custom_steps=custom_steps)
        widget.setObjectName(self.name+"_"+name)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_progress_bar(self, name, value=None, label=None, location="next", tooltip=None, add_change_event=True, virtual=False):
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
        widget.setObjectName(self.name+"_"+name)
        if value is not None:
            widget.setValue(value)
        return self.add_simple_widget(name,widget,label=label,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_combo_box(self, name, value=None, options=None, index_values=None, label=None, add_indicator=None, location="next", tooltip=None, add_change_event=True, virtual=False):
        """
        Add a combo box to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            options (list): list of string specifying box options
            index_values (list): list of values corresponding to box options; if supplies, these number are used when setting/getting values or sending signals.
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=combo_box.ComboBox(self)
        widget.setObjectName(self.name+"_"+name)
        if options:
            widget.addItems(options)
            if index_values is not None:
                widget.set_index_values(index_values)
            if value is not None:
                widget.setCurrentIndex(value)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)

    def add_spacer(self, height=0, width=0, stretch_height=False, stretch_width=False, location="next"):
        """
        Add a spacer with the given width and height to the given location.
        
        If ``stretch_height==True`` or ``stretch_width==True``, the widget will stretch in these directions; otherwise, the widget size is fixed.
        """
        spacer=QtWidgets.QSpacerItem(width,height,
            QtWidgets.QSizePolicy.MinimumExpanding if stretch_width else QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.MinimumExpanding if stretch_height else QtWidgets.QSizePolicy.Minimum)
        lname,location=self._normalize_location(location)
        self._insert_layout_element(lname,spacer,location,kind="item")
        return spacer
    def add_padding(self, kind="vertical", location="next"):
        """Add a padding (expandable spacer) of the given kind (``"vertical"`` or ``"horizontal"``) to the given location"""
        if kind=="vertical":
            self.add_spacer(stretch_height=True,location=location)
        elif kind=="horizontal":
            self.add_spacer(stretch_width=True,location=location)
    def add_decoration_label(self, text, location="next"):
        """Add a text label (only for decoration) with the given text"""
        label=QtWidgets.QLabel(self)
        label.setText(str(text))
        label.setAlignment(QtCore.Qt.AlignLeft)
        lname,location=self._normalize_location(location)
        self._insert_layout_element(lname,label,location)
        return label
    def insert_row(self, row, sublayout=None):
        """Insert a new table row at the given location"""
        if sublayout is None:
            layout=self.formLayout
        else:
            layout,kind=self._sublayouts[sublayout]
            if kind!="grid":
                raise ValueError("only grid layouts are allowed (hbox layouts work automatically)")
        utils.insert_layout_row(layout,row%(layout.rowCount() or 1))

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
    def get_value(self, name=None):
        """Get value of a widget with the given name"""
        return self.gui_values.get_value((self.gui_values_root,name or ""),include=self.params)
    @controller.gui_thread_method
    def get_all_values(self, name=None):
        """Get value of all widget in the given branch"""
        return self.gui_values.get_all_values((self.gui_values_root,name or ""),include=self.params)
    @controller.gui_thread_method
    def set_value(self, name, value, force=False):
        """
        Set value of a widget with the given name
        
        If ``force==True``, force widget value (e.g., ignoring restriction on not changing values of focused widgets)
        """
        par=self.params[name]
        if force or par.value_handler.can_set_value(allow_focus=self.change_focused_control):
            return self.gui_values.set_value((self.gui_values_root,name),value)
    @controller.gui_thread_method
    def set_all_values(self, value, force=False):
        """Set values of all widgets in the table"""
        for n,v in dictionary.as_dictionary(value).iternodes(to_visit="all",topdown=True,include_path=True):
            path="/".join(n)
            if path in self.params:
                self.set_value(path,v,force=force)

    def get_handler(self, name):
        """Get value handler of a widget with the given name"""
        return self.params[name].value_handler
    def get_widget(self, name):
        """Get a widget with the given name"""
        return self.params[name].widget
    def get_value_changed_signal(self, name):
        """Get a value-changed signal for a widget with the given name"""
        return self.params[name].value_handler.get_value_changed_signal()

    @controller.gui_thread_method
    def get_indicator(self, name=None):
        """Get indicator value for a widget with the given name"""
        return self.gui_values.get_indicator((self.gui_values_root,name or ""),include=self.params)
    @controller.gui_thread_method
    def get_all_indicators(self, name=None):
        """Get indicator values of all widget in the given branch"""
        return self.gui_values.get_all_indicators((self.gui_values_root,name or ""),include=self.params)
    @controller.gui_thread_method
    def set_indicator(self, name, value, ignore_missing=True):
        """Set indicator value for a widget or a branch with the given name"""
        return self.gui_values.set_indicator((self.gui_values_root,name or ""),value,include=self.params,ignore_missing=ignore_missing)
    set_all_indicators=set_indicator
    @controller.gui_thread_method
    def update_indicators(self):
        """Update all indicators to represent current values"""
        return self.gui_values.update_indicators(root=self.gui_values_root,include=self.params)

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
                path=(self.gui_values_root,name)
                self.gui_values.remove_handler(path)
                self.gui_values.remove_indicator_handler(path)
            self.params={}
            utils.clean_layout(self.formLayout,delete_layout=True)
            self.formLayout=QtWidgets.QGridLayout(self)
            self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            self.formLayout.setContentsMargins(5,5,5,5)
            self.formLayout.setSpacing(5)
            self.formLayout.setObjectName(self.name+"_formLayout")
            self._sublayouts={}
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
        threadprop.current_controller().subscribe_sync(update_text,srcs=srcs,tags=tags,dsts="any",filt=filt,limit_queue=10)