from . import edit, label as widget_label, combo_box, button as widget_button
from . import container
from ...thread import threadprop, controller
from .. import value_handling
from ...utils import py3, dictionary

from .. import QtWidgets

import collections
import contextlib


class ParamTable(container.QWidgetContainer):
    """
    GUI parameter table.
    
    Simplifies creating code-generated controls and displays table layouts.
    
    Has methods for adding various kinds of controls (labels, edit boxes, combo boxes, check boxes),
    automatically creates values table for easy settings/getting.
    By default supports 2-column (label-control) and 3-column (label-control-indicator) layout, depending on the parameters given to :meth:`setup`.

    Similar to :class:`.GUIValues`, has three container-like accessor:
    ``.h`` for getting the value handler
    (i.e., ``self.get_handler(name)`` is equivalent to ``self.h[name]``),
    ``.w`` for getting the underlying widget
    (i.e., ``self.get_widget(name)`` is equivalent to ``self.w[name]``),
    ``.v`` for settings/getting values using the default getting method
    (equivalent to ``.wv`` if ``cache_values=False`` in :meth:`setup`, and to ``.cv`` otherwise),
    ``.wv`` for settings/getting current current widget values without caching
    (i.e., ``self.get_value(name)`` is equivalent to ``self.v[name]``, and ``self.set_value(name, value)`` is equivalent to ``self.v[name]=value``),
    ``.cv`` for settings/getting values using cached value's table for getting
    (i.e., ``self.current_values[name]`` is equivalent to ``self.cv[name]``, and ``self.set_value(name, value)`` is equivalent to ``self.cv[name]=value``),
    (i.e., ``self.get_value(name)`` is equivalent to ``self.v[name]``, and ``self.set_value(name, value)`` is equivalent to ``self.v[name]=value``),
    ``.i`` for settings/getting indicator values
    (i.e., ``self.get_indicator(name)`` is equivalent to ``self.i[name]``, and ``self.set_indicator(name, value)`` is equivalent to ``self.i[name]=value``)
    ``.vs`` for getting the value changed Qt signal
    (i.e., ``self.get_value_changed_signal(name)`` is equivalent to ``self.s[name]``),

    Like most widgets, requires calling :meth:`setup` to set up before usage.

    Args:
        parent: parent widget
    """
    def __init__(self, parent=None, name=None):
        self.params={}
        super().__init__(parent,name=name)
        self.h=dictionary.ItemAccessor(self.get_handler)
        self.w=dictionary.ItemAccessor(self.get_widget)
        self.iw=dictionary.ItemAccessor(self.get_indicator_widget)
        self.lw=dictionary.ItemAccessor(self.get_label_widget)
        self.wv=dictionary.ItemAccessor(self.get_value,self.set_value)
        self.v=self.wv
        self.cv=dictionary.ItemAccessor(lambda name: self.current_values[name],self.set_value)
        self.i=dictionary.ItemAccessor(self.get_indicator,self.set_indicator)
        self.vs=dictionary.ItemAccessor(self.get_value_changed_signal)
    def _make_new_layout(self, kind, *args, **kwargs):
        layout=super()._make_new_layout(kind,*args,**kwargs)
        if kind=="grid":
            layout.setSpacing(5)
        return layout
    def _set_main_layout(self):
        super()._set_main_layout()
        self.main_layout.setContentsMargins(5,5,5,5)
        self.main_layout.setColumnStretch(1,1)
    def setup(self, name=None, add_indicator=True, gui_thread_safe=False, cache_values=False, change_focused_control=False):  # pylint: disable=arguments-differ, arguments-renamed
        """
        Setup the table.

        Args:
            name (str): table widget name
            add_indicator (bool): if ``True``, add indicators for all added widgets by default.
            gui_thread_safe (bool): if ``True``, all value-access and indicator-access calls
                (``get/set_value``, ``get/set_all_values``, ``get/set_indicator``, and ``update_indicators``) are automatically called in the GUI thread.
            cache_values (bool): if ``True`` or ``"update_one"``, store a dictionary with all the current values and update it every time a GUI value is changed;
                provides a thread-safe way to check current parameters without lag
                (unlike :meth:`get_value` or :meth:`get_all_values` with ``gui_thread_safe==True``, which re-route calls to a GUI thread and may cause up to 100ms delay)
                can also be set to ``"update_all"``, in which case change of any value will cause value update of all variables;
                otherwise, change of a value will only cause update of that same value (might potentially miss some value updates for custom controls).
            change_focused_control (bool): if ``False`` and :meth:`set_value` method is called while the widget has user focus, ignore the value;
                note that :meth:`set_all_values` will still set the widget value.
        """
        super().setup(name=name,layout="grid")
        self.add_indicator=add_indicator
        self.gui_thread_safe=gui_thread_safe
        self.change_focused_control=change_focused_control
        self.cache_values=cache_values
        self.current_values=dictionary.Dictionary()
        self.v=self.cv if cache_values else self.wv

    @controller.exsafeSlot()
    def _update_cache_values(self, name=None, value=None):  # pylint: disable=unused-argument
        if self.cache_values:
            if name is None or self.cache_values=="update_all":
                self.current_values=self.get_all_values()
            else:
                self.current_values[name]=self.get_value(name)

    def add_sublayout(self, name, kind="grid", location=("next",0,1,"end")):
        return super().add_sublayout(name,kind=kind,location=location)
    @contextlib.contextmanager
    def using_new_sublayout(self, name, kind="grid", location=("next",0,1,"end")):
        with super().using_new_sublayout(name,kind=kind,location=location):
            yield

    def pad_borders(self, kind="both", stretch=0):
        """
        Add expandable paddings on the bottom and/or right border.

        `kind` can be ``"bottom"``, ``"right"``, ``"both"``, or ``"none"`` (do nothing).
        Note that if more elements are added, they will be placed after the padding, so the table will be padded in the middle.
        """
        if kind in ["bottom","both"]:
            self.add_padding("vertical",location=("next",0),stretch=stretch)
        if kind in ["right","both"]:
            self.add_padding("horizontal",location=(0,"next"),stretch=stretch)

    def add_frame(self, name, layout="vbox", location=("next",0,1,"end"), gui_values_path=True, no_margins=True):
        return super().add_frame(name,layout=layout,location=location,gui_values_path=gui_values_path,no_margins=no_margins)
    def add_group_box(self, name, caption, layout="vbox", location=("next",0,1,"end"), gui_values_path=True, no_margins=True):
        return super().add_group_box(name,caption,layout=layout,location=location,gui_values_path=gui_values_path,no_margins=no_margins)

    ParamRow=collections.namedtuple("ParamRow",["widget","label","indicator","value_handler","indicator_handler"])
    def _add_widget(self, name, params, add_change_event=True):
        name=self._normalize_name(name)
        self.params[name]=params
        if params.widget is not None:
            self.add_child(name,params.widget,location="skip",gui_values_path=False)
        self.gui_values.add_handler(name,params.value_handler)
        if params.indicator_handler:
            self.gui_values.add_indicator_handler(name,params.indicator_handler)
        if add_change_event:
            params.value_handler.connect_value_changed_handler(lambda value: self.contained_value_changed.emit(name,value),only_signal=True)
        if self.cache_values:
            params.value_handler.connect_value_changed_handler(lambda value: self._update_cache_values(name,value),only_signal=False)
        self._update_cache_values()
    def add_simple_widget(self, name, widget, label=None, value_handler=None, add_indicator=None, location=None, tooltip=None, add_change_event=True):
        """
        Add a 'simple' (single-spaced, single-valued) widget to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            widget: widget to add
            label (str): if not ``None``, specifies label to put in front of the widget in the layout
            value_handler: value handler of the widget; by default, use auto-detected value handler (works for many simple built-in or custom widgets)
            add_indicator: if ``True``, add an indicator label in the third column and a corresponding indicator handler in the built-in values table;
                by default, use the default value supplied to :meth:`setup`
            location (tuple): tuple ``(row, column)`` specifying location of the widget (or widget label, if it is specified);
                by default, add to a new row in the end and into the first column
                can also be a string ``"skip"``, which means that the widget is added to some other location manually later
                (this option only works if ``label=None``, and doesn't add any indicator)
            tooltip: widget tooltip (mouseover text)
            add_change_event (bool): if ``True``, changing of the widget's value emits the table's ``contained_value_changed`` event
        
        Return the widget's value handler
        """
        name=self._normalize_name(name)
        if name in self.params:
            raise KeyError("widget {} already exists".format(name))
        if add_indicator is None:
            add_indicator=self.add_indicator
        if isinstance(location,dict):
            llocation=location.get("label",None)
            ilocation=location.get("indicator",None)
            location=location.get("widget",None)
        else:
            ilocation=llocation=None
        lname,location=self._normalize_location(location,default_location=("next",0,1,3 if add_indicator else 2))
        if location!="skip":
            row,col,rowspan,colspan=location
            labelspan=1 if label is not None else 0
            indspan=1 if (add_indicator and ilocation is None) else 0
            if colspan<indspan+labelspan+1:
                raise ValueError("column span {} should be at least {} to accommodate the widget, the label, and the indicator".format(colspan,indspan+labelspan+1))
        else:
            if label is not None:
                raise ValueError("label can not be combined with 'skip' location")
            add_indicator=False
        if add_indicator and ilocation!="next_line":
            ilname,ilocation=self._normalize_location(ilocation,default_location=(row,col+colspan-1,rowspan,1),default_layout=lname)
        if label is not None:
            wlabel=QtWidgets.QLabel(self)
            wlabel.setObjectName("{}__label".format(name))
            llname,llocation=self._normalize_location(llocation,default_location=(row,col,rowspan,1),default_layout=lname)
            self._insert_layout_element(llname,wlabel,llocation)
            wlabel.setText(label)
        else:
            wlabel=None
        if location!="skip":
            self._insert_layout_element(lname,widget,(row,col+labelspan,rowspan,colspan-labelspan-indspan))
        value_handler=value_handler or value_handling.create_value_handler(widget)
        if add_indicator:
            windicator=QtWidgets.QLabel(self)
            windicator.setObjectName("{}__indicator".format(name))
            if ilocation=="next_line":
                ilname,ilocation=self._normalize_location((row+1,col+labelspan,1,colspan-labelspan),default_location=(row,col+colspan-1,rowspan,1),default_layout=lname)
            self._insert_layout_element(ilname,windicator,ilocation)
            indicator_handler=value_handling.LabelIndicatorHandler(windicator,formatter=value_handler if add_indicator==True else add_indicator)
        else:
            windicator=None
            indicator_handler=None
        if tooltip is not None:
            if wlabel is not None:
                wlabel.setToolTip(tooltip)
            else:
                widget.setToolTip(tooltip)
        self._add_widget(name,self.ParamRow(widget,wlabel,windicator,value_handler,indicator_handler),add_change_event=add_change_event)
        return value_handler

    def add_custom_widget(self, name, widget, value_handler=None, indicator_handler=None, location=None, tooltip=None, add_change_event=True):
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
            add_change_event (bool): if ``True``, changing of the widget's value emits the table's ``contained_value_changed`` event
        
        Return the widget's value handler
        """
        name=self._normalize_name(name)
        if name in self.params:
            raise KeyError("widget {} already exists".format(name))
        lname,location=self._normalize_location(location,default_location=("next",0,1,3))
        if location!="skip":
            self._insert_layout_element(lname,widget,location)
        value_handler=value_handler or value_handling.create_value_handler(widget)
        indicator_handler=indicator_handler or value_handling.create_indicator_handler(widget)
        if tooltip is not None:
            widget.setToolTip(tooltip)
        self._add_widget(name,self.ParamRow(widget,None,None,value_handler,indicator_handler),add_change_event=add_change_event)
        return value_handler
    def remove_widget(self, name):
        """Remove the widget and, if applicable, its indicator and label"""
        name=self._normalize_name(name)
        par=self.params.pop(name)
        self.gui_values.remove_handler(name,remove_indicator=True)
        if par.widget is not None:
            self.remove_child(name)
        if par.label is not None:
            self.remove_layout_element(par.label)
        if par.indicator is not None:
            self.remove_layout_element(par.indicator)
    def add_virtual_element(self, name, value=None, multivalued=False, add_indicator=None):
        """
        Add a virtual table element.

        Doesn't correspond to any actual widget, but behaves very similarly from the application point of view
        (its value can be set or read, it has on-change events, it can have indicator).
        The element value is simply stored on set and retrieved on get.
        If ``multivalued==True``, the internal value is assumed to be complex, so it is forced to be a :class:`.Dictionary` every time it is set.
        If ``add_indicator==True``, add default indicator handler as well.
        """
        value_handler=value_handling.VirtualValueHandler(value,multivalued=multivalued)
        if add_indicator is None:
            add_indicator=self.add_indicator
        indicator_handler=value_handling.VirtualIndicatorHandler(multivalued=multivalued) if add_indicator else None
        self._add_widget(name,self.ParamRow(None,None,None,value_handler,indicator_handler))
    def add_property_element(self, name, getter=None, setter=None, add_indicator=True):
        """
        Add a property value element.

        Doesn't correspond to any actual widget, but behaves very similarly from the application point of view;
        each time the value is set or get, the corresponding setter and getter methods are called.
        If ``add_indicator==True``, add default (stored value) indicator handler as well.
        """
        value_handler=value_handling.PropertyValueHandler(getter=getter,setter=setter)
        if add_indicator is None:
            add_indicator=self.add_indicator
        indicator_handler=value_handling.VirtualIndicatorHandler if add_indicator else None
        self._add_widget(name,self.ParamRow(None,None,None,value_handler,indicator_handler))
    def add_button(self, name, caption, label=None, add_indicator=None, location=None, tooltip=None, add_change_event=True, virtual=False):
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
    def add_toggle_button(self, name, caption, value=False, label=None, add_indicator=None, location=None, tooltip=None, add_change_event=True, virtual=False):
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
    def add_dropdown_button(self, name, caption, options=None, index_values=None, label=None, add_indicator=None, location=None, tooltip=None, add_change_event=True, virtual=False):
        """
        Add a button which shows a dropdown menu when clicked.

        Similar in behavior to a regular button, but its changed event provides a single argument which is the name of the selected item.
        
        Args:
            name (str): widget name (used to reference its value in the values table)
            caption (str or list): text on the button
            options (list): list of strings specifying menu options
            index_values (list): list of values corresponding to menu options; if supplied, these values are used when setting/getting values or sending signals.
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,add_indicator=add_indicator)
        widget=widget_button.DropdownButton(self)
        widget.setText(caption)
        widget.setObjectName(self.name+"_"+name)
        if options:
            if index_values is None:
                index_values=list(range(len(options)))
            for i,o in zip(index_values,options):
                widget.add_item(i,o)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_check_box(self, name, caption, value=False, label=None, add_indicator=None, location=None, tooltip=None, add_change_event=True, virtual=False):
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
    def add_text_label(self, name, value="", label=None, location=None, tooltip=None, add_change_event=False, virtual=False):
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
    def add_enum_label(self, name, options, value=None, out_of_range="error", prep=None, label=None, location=None, tooltip=None, add_change_event=False, virtual=False):
        """
        Add a text label to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            options (list): dictionary ``{option: index_value}`` which converts values into text
            out_of_range (str): behavior when out-of-range value is applied;
                can be ``"error"`` (raise error), ``"text"`` (convert value into text), or ``"ignore"`` (keep current value).
            prep: a function which takes a single value argument and converts into an option; useful for "fuzzy" options (e.g., when 0 and ``False`` mean the same thing)
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value)
        widget=widget_label.EnumLabel(self,options=options,value=value,prep=prep)
        widget.set_out_of_range(out_of_range)
        widget.setObjectName(self.name+"_"+name)
        return self.add_simple_widget(name,widget,label=label,add_indicator=False,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_num_label(self, name, value=0, limiter=None, formatter=None, label=None, tooltip=None, location=None, add_change_event=False, virtual=False):
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
    def add_text_edit(self, name, value="", label=None, multiline=False, add_indicator=None, location=None, tooltip=None, add_change_event=True, virtual=False):
        """
        Add a text edit to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value (bool): specifies initial value
            multiline (bool): if ``True``, use multi-line text edit widget; otherwise, use a standard single-line edit
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=edit.TextEdit(self,value=value) if not multiline else edit.MultilineTextEdit(self,value=value)
        widget.setObjectName(self.name+"_"+name)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)
    def add_num_edit(self, name, value=None, limiter=None, formatter=None, custom_steps=None, label=None, add_indicator=None, location=None, tooltip=None, add_change_event=True, virtual=False):
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
    def add_progress_bar(self, name, value=None, label=None, location=None, tooltip=None, add_change_event=True, virtual=False):
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
    def add_combo_box(self, name, value=None, options=None, index_values=None, out_of_range="reset", label=None, add_indicator=None, location=None, tooltip=None, add_change_event=True, virtual=False):
        """
        Add a combo box to the table.

        Args:
            name (str): widget name (used to reference its value in the values table)
            value: specifies initial value
            options (list): list of strings specifying box options or a dictionary ``{option: index_value}``
            index_values (list): list of values corresponding to box options; if supplied, these values are used when setting/getting values or sending signals;
                if `options` is a dictionary, this parameter is ignored
            out_of_range (str): behavior when out-of-range value is applied;
                can be ``"error"`` (raise error), ``"reset"`` (reset to no-value position), or ``"ignore"`` (keep current value).
            virtual (bool): if ``True``, the widget is not added, and a virtual handler is added instead
            
        Rest of the arguments and the return value are the same as :meth:`add_simple_widget`.
        """
        if virtual:
            return self.add_virtual_element(name,value=value,add_indicator=add_indicator)
        widget=combo_box.ComboBox(self)
        widget.setObjectName(self.name+"_"+name)
        widget.set_out_of_range(action=out_of_range)
        if options is not None:
            widget.set_options(options,index_values=index_values)
            if value is not None:
                widget.set_value(value)
            else:
                index_values=widget.get_index_values()
                widget.set_value(index_values[0] if index_values else 0)
        return self.add_simple_widget(name,widget,label=label,add_indicator=add_indicator,location=location,tooltip=tooltip,add_change_event=add_change_event)

    def _expand_names_list(self, names):
        if isinstance(names,py3.anystring):
            names=[names]
        if names is None:
            names=self.params.keys()
        return names
    def set_enabled(self, names=None, enabled=True, include_indicator=True, include_label=True):
        """Enable or disable widgets with the given names (by default, all widgets)"""
        for name in self._expand_names_list(names):
            name=self._normalize_name(name)
            par=self.params[name]
            if par.widget is not None:
                par.widget.setEnabled(enabled)
            if include_label and par.label is not None:
                par.label.setEnabled(enabled)
            if include_indicator and par.indicator is not None:
                par.indicator.setEnabled(enabled)
    def set_visible(self, names=None, visible=True, include_indicator=True, include_label=True):
        """Show or hide widgets with the given names (by default, all widgets)"""
        for name in self._expand_names_list(names):
            name=self._normalize_name(name)
            par=self.params[name]
            if par.widget is not None:
                par.widget.setVisible(visible)
            if include_label and par.label is not None:
                par.label.setVisible(visible)
            if include_indicator and par.indicator is not None:
                par.indicator.setVisible(visible)

    @controller.gui_thread_method
    def get_value(self, name=None):
        return super().get_value(name=name)
    @controller.gui_thread_method
    def get_all_values(self):
        return super().get_all_values()
    @controller.gui_thread_method
    def set_value(self, name, value, force=False):  # pylint: disable=arguments-differ
        """
        Set value of a widget with the given name.
        
        If ``force==True``, force widget value (e.g., ignoring restriction on not changing values of focused widgets)
        """
        if not force:
            return super().set_value(name,value)
        if name is None:
            self.set_all_values(value,force=force)
        name=self._normalize_name(name)
        try:
            par=self.params[name]
            allow_set=par.value_handler.can_set_value(allow_focus=self.change_focused_control)
        except KeyError:
            allow_set=True
        if allow_set:
            return super().set_value(name,value)
    @controller.gui_thread_method
    def set_all_values(self, value, force=False):  # pylint: disable=arguments-differ
        """
        Set values of all widgets in the table.
        
        If ``force==True``, force widget value (e.g., ignoring restriction on not changing values of focused widgets)
        """
        if not force:
            return super().set_all_values(value)
        for n,v in dictionary.as_dictionary(value).iternodes(to_visit="all",topdown=True,include_path=True):
            path="/".join(n)
            try:
                self.set_value(path,v,force=force)
            except KeyError:
                pass
    @controller.gui_thread_method
    def update_value(self, name=None):
        return super().update_value(name=name)

    def get_widget(self, name):
        name=self._normalize_name(name)
        try:
            return self.params[name].widget
        except KeyError:
            return super().get_widget(name)
    def get_indicator_widget(self, name):
        """Get indicator widget for a parameter with the given name, or ``None`` if this parameter has no indicator label"""
        name=self._normalize_name(name)
        return self.params[name].indicator
    def get_label_widget(self, name):
        """Get label widget for a parameter with the given name, or ``None`` if this parameter has no label"""
        name=self._normalize_name(name)
        return self.params[name].label

    def get_child(self, name):
        name=self._normalize_name(name)
        if name in self.params:
            return self.get_widget(name)
        return super().get_child(name)
    def remove_child(self, name):
        name=self._normalize_name(name)
        if name in self.params:
            return self.remove_widget(name)
        return super().remove_child(name)

    @controller.gui_thread_method
    def get_indicator(self, name=None):
        return super().get_indicator(name=name)
    @controller.gui_thread_method
    def get_all_indicators(self):
        return super().get_all_indicators()
    @controller.gui_thread_method
    def set_indicator(self, name, value, ignore_missing=False):
        return super().set_indicator(name,value,ignore_missing=ignore_missing)
    @controller.gui_thread_method
    def set_all_indicators(self, value, ignore_missing=True):
        return super().set_all_indicators(value,ignore_missing=ignore_missing)
    @controller.gui_thread_method
    def update_indicators(self):
        return super().update_indicators()

    def clear(self, disconnect=False):  # pylint: disable=arguments-differ
        """
        Clear the table (remove all widgets)
        
        If ``disconnect==True``, also disconnect all slots connected to the ``contained_value_changed`` signal.
        """
        if self.params:
            if disconnect:
                try:
                    self.contained_value_changed.disconnect()
                except (TypeError,RuntimeError): # no signals connected
                    pass
            for name in self.params:
                self.gui_values.remove_handler(name,remove_indicator=True)
            self.params={}
            super().clear()
            self._update_cache_values()
        else:
            super().clear()

    def __contains__(self, name):
        name=self._normalize_name(name)
        return name in self.params



class StatusTable(ParamTable):
    """
    Expansion of :class:`ParamTable` which adds status lines, which automatically subscribe to signals and update values.
    """
    def setup(self, name=None, add_indicator=True, gui_thread_safe=False, cache_values=False, change_focused_control=False):
        super().setup(name=name,add_indicator=add_indicator,gui_thread_safe=gui_thread_safe,cache_values=cache_values,change_focused_control=change_focused_control)
        self._status_line_params={}
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
            self.v[name]=fmt(src,tag,value) if fmt is not None else value
        self._status_line_params[name]=(srcs,tags,update_text)
        threadprop.current_controller().subscribe_sync(update_text,srcs=srcs,tags=tags,filt=filt,limit_queue=10)
    def update_status_line(self, name, thread=None, path=None):
        """
        Update status line to the variable with the given `path` from the thread with the given `thread` name.

        If `thread` is ``None``, use ``srcs`` name provided upon creation.
        If `path` is ``None``, use ``tags`` name provided upon creation.
        """
        srcs,tags,update_text=self._status_line_params[name]
        thread=thread or srcs
        path=path or tags
        try:
            ctl=controller.get_controller(thread,sync=False)
            value=ctl.get_variable(path)
            if value is not None:
                self.v[name]=update_text(srcs,tags,value) if update_text is not None else value
        except threadprop.NoControllerThreadError:
            pass