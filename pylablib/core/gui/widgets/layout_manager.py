from .. import utils
from ...utils import py3, funcargparse

from .. import QtCore, QtWidgets

import contextlib


class IQLayoutManagedWidget:
    """
    GUI widget which can manage layouts.

    Typically, first it is set up using :meth:`setup` method to specify the master layout kind;
    afterwards, widgets and sublayout can be added using :meth:`add_to_layout`.
    In addition, it can directly add named sublayouts using :meth:`add_sublayout` method.
    
    Abstract mix-in class, which needs to be added to a class inheriting from ``QWidget``.
    Alternatively, one can directly use :class:`QLayoutManagedWidget`, which already inherits from ``QWidget``.
    """
    def __init__(self, *args, **kwargs):
        if not isinstance(self,QtWidgets.QWidget):
            raise RuntimeError("IQLayoutManagedWidget should be mixed with a QWidget class or subclass")
        super().__init__(*args,**kwargs)
        self.main_layout=None
        self._default_layout="main"
    
    def _make_new_layout(self, kind, *args, **kwargs):
        """Make a layout of the given kind"""
        if kind=="grid":
            return QtWidgets.QGridLayout(*args,**kwargs)
        if kind=="vbox":
            return QtWidgets.QVBoxLayout(*args,**kwargs)
        if kind=="hbox":
            return QtWidgets.QHBoxLayout(*args,**kwargs)
        raise ValueError("unrecognized layout kind: {}".format(kind))
    def _set_main_layout(self):
        self.main_layout=self._make_new_layout(self.main_layout_kind,self)
        name=getattr(self,"name",None)
        self.main_layout.setObjectName(name+"_main_layout" if name else "main_layout")
        if self.no_margins:
            self.main_layout.setContentsMargins(0,0,0,0)
    def setup(self, layout="grid", no_margins=False):
        """
        Setup the layout.

        Args:
            layout: layout kind; can be ``"grid"``, ``"vbox"`` (vertical single-column box), or ``"hbox"`` (horizontal single-row box).
            no_margins: if ``True``, set all layout margins to zero (useful when the widget is in the middle of layout hierarchy)
        """
        self.main_layout_kind=layout
        self.no_margins=no_margins
        self._set_main_layout()
        self._sublayouts={"main":(self.main_layout,self.main_layout_kind)}
        self._spacers=[]

    @contextlib.contextmanager
    def using_layout(self, name):
        """Use a different sublayout as default inside the ``with`` block"""
        current_layout,self._default_layout=self._default_layout,name
        try:
            yield
        finally:
            self._default_layout=current_layout
    def _normalize_location(self, location, default_location=None, default_layout=None):
        if location=="skip":
            return None,"skip"
        if not isinstance(location,(list,tuple)):
            location=() if location is None else (location,)
        if location and isinstance(location[0],py3.textstring) and location[0]!="next":
            lname,location=location[0],location[1:]
        else:
            lname=default_layout or self._default_layout
        layout,lkind=self._sublayouts[lname]
        if default_location is None:
            default_location=("next",0,1,1)
        location+=(None,)*(4-len(location))
        location=[d if l is None else l for (l,d) in zip(location,default_location)]
        row,col,rowspan,colspan=location
        if lkind=="grid":
            row_cnt,col_cnt=layout.rowCount(),layout.columnCount()
        elif lkind=="vbox":
            col,colspan=0,1
            row_cnt,col_cnt=layout.count(),1
        else:
            if col==0:
                col=row
            if colspan==1:
                colspan=rowspan
            row,rowspan=0,1
            row_cnt,col_cnt=1,layout.count()
        if lkind in {"grid","vbox"}:
            if row=="next":
                row=row_cnt if layout.count() else 0
            else:
                row=(row%max(row_cnt,1) if row<0 else row)
            if rowspan=="end":
                rowspan=max(row_cnt-row,1)
            elif rowspan<0:
                rowspan=max(row_cnt+rowspan-row,1)
        if lkind in {"grid","hbox"}:
            if col=="next":
                col=col_cnt if layout.count() else 0
            else:
                col=(col%max(col_cnt,1) if col<0 else col)
            if colspan=="end":
                colspan=max(col_cnt-col,1)
            elif colspan<0:
                colspan=max(col_cnt+colspan-col,1)
        return lname,(row,col,rowspan,colspan)
    def _insert_layout_element(self, lname, element, location, kind="widget"):
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
            if lkind=="vbox" and (location[1]!=0 or location[3]!=1):
                raise ValueError("vbox layout only has one column")
            if lkind=="hbox" and (location[0]!=0 or location[2]!=1):
                raise ValueError("hbox layout only has one row")
            if kind=="widget":
                layout.insertWidget(idx,element)
            elif kind=="item":
                layout.insertItem(idx,element)
            elif kind=="layout":
                layout.insertLayout(idx,element)
            else:
                raise ValueError("unrecognized element kind: {}".format(kind))
    def add_to_layout(self, element, location=None, kind="widget"):
        """
        Add an existing `element` to the layout at the given `location`.

        `kind` can be ``"widget"`` for widgets, ``"layout"`` for other layouts, or ``"item"`` for layout items (spacers).
        """
        lname,location=self._normalize_location(location)
        if location!="skip":
            self._insert_layout_element(lname,element,location,kind=kind)
        return element
    def remove_layout_element(self, element):
        """Remove a previously added layout element"""
        for layout,_ in self._sublayouts.values():
            idx=utils.find_layout_element(layout,element)
            if idx is not None:
                utils.delete_layout_item(layout,idx)
                return True
        return False
    def get_element_position(self, element):
        """
        Get the sublayout and the position of the given widget.
        
        Return tuple ``(sublayout, location)``, where ``sublayout`` is the sublayout name (``"name"`` for the main layout),
        and ``location`` is a tuple ``(row, column, rowspan, colspan)``.
        If the given widget is not in this layout, return ``None``.
        """
        for name,(layout,kind) in self._sublayouts.items():
            idx=utils.find_layout_element(layout,element)
            if idx is not None:
                if kind=="grid":
                    location=layout.getItemPosition(idx)
                elif kind=="hbox":
                    location=(0,idx,1,1)
                elif kind=="vbox":
                    location=(idx,0,1,1)
                return name,location 
        return None
    def add_sublayout(self, name, kind="grid", location=None):
        """
        Add a sublayout to the given location.

        `name` specifies the sublayout name, which can be used to refer to it in specifying locations later.
        `kind` can be ``"grid"``, ``"vbox"`` (vertical single-column box), or ``"hbox"`` (horizontal single-row box).
        """
        if name in self._sublayouts:
            raise ValueError("sublayout {} already exists".format(name))
        layout=self._make_new_layout(kind)
        layout.setContentsMargins(0,0,0,0)
        layout.setObjectName(name)
        self.add_to_layout(layout,location,kind="layout")
        self._sublayouts[name]=(layout,kind)
        return layout
    @contextlib.contextmanager
    def using_new_sublayout(self, name, kind="grid", location=None):
        """
        Create a different sublayout and use it as default inside the ``with`` block.

        `kind` can be ``"grid"``, ``"vbox"`` (vertical single-column box), or ``"hbox"`` (horizontal single-row box).
        """
        self.add_sublayout(name,kind=kind,location=location)
        with self.using_layout(name):
            yield
    def get_sublayout(self, name=None):
        """Get the previously added sublayout"""
        return self._sublayouts[name or self._default_layout][0]
    def get_sublayout_kind(self, name=None):
        """Get the kind of the previously added sublayout"""
        return self._sublayouts[name or self._default_layout][1]
    def get_layout_shape(self, name=None):
        """Get shape ``(rows, cols)`` of the current layout"""
        layout,kind=self._sublayouts[name or self._default_layout]
        if kind=="grid":
            return layout.rowCount(),layout.columnCount()
        elif kind=="hbox":
            return 1,layout.count()
        else:
            return layout.count(),1
    
    def add_spacer(self, height=0, width=0, stretch_height=False, stretch_width=False, stretch=0, location="next"):
        """
        Add a spacer with the given width and height to the given location.
        
        If ``stretch_height==True`` or ``stretch_width==True``, the widget will stretch in these directions; otherwise, the widget size is fixed.
        If `stretch` is not ``None``, it specifies stretch of the spacer the corresponding direction (applied to the upper row and leftmost column for multi-cell spacer);
        if `kind=="both"``, it can also be a tuple with two stretches along vertical and horizontal directions.
        """
        spacer=QtWidgets.QSpacerItem(width,height,
            QtWidgets.QSizePolicy.MinimumExpanding if stretch_width else QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.MinimumExpanding if stretch_height else QtWidgets.QSizePolicy.Minimum)
        lname,lpos=self._normalize_location(location)
        self.add_to_layout(spacer,location,kind="item")
        self._spacers.append(spacer)  # otherwise the reference is lost, and the object might be deleted
        if lname is not None:
            r,c=lpos[:2]
            layout,lkind=self._sublayouts[lname]
            if not isinstance(stretch,tuple):
                stretch=(stretch,stretch)
            if lkind=="grid":
                if stretch_height:
                    layout.setRowStretch(r,stretch[0])
                if stretch_width:
                    layout.setColumnStretch(c,stretch[1])
            elif lkind=="vbox" and stretch_height:
                layout.setStretch(r,stretch[0])
            elif lkind=="hbox" and stretch_width:
                layout.setStretch(c,stretch[1])
        return spacer
    def add_padding(self, kind="auto", location="next", stretch=0):
        """
        Add a padding (expandable spacer) of the given kind to the given location.
        
        `kind` can be ``"vertical"``, ``"horizontal"``, ``"auto"`` (vertical for ``grid`` and ``vbox`` layouts, horizontal for ``hbox``),
        or ``"both"`` (stretches in both directions).
        If `stretch` is not ``None``, it specifies stretch of the spacer the corresponding direction (applied to the upper row and leftmost column for multi-cell spacer);
        can also be a tuple with two stretches along vertical and horizontal directions.
        """
        funcargparse.check_parameter_range(kind,"kind",{"auto","horizontal","vertical","both"})
        if kind=="auto":
            lname,_=self._normalize_location(location)
            if lname is None:
                kind="vertical"
            else:
                _,lkind=self._sublayouts[lname]
                kind="horizontal" if lkind=="hbox" else "vertical"
        stretch_height=kind in {"vertical","both"}
        stretch_width=kind in {"horizontal","both"}
        return self.add_spacer(stretch_height=stretch_height,stretch_width=stretch_width,location=location,stretch=stretch)
    def _normalize_stretch(self, args):
        if len(args)==1:
            return list(enumerate(args[0]))
        if len(args)==2:
            return [(args[0],args[1])]
        raise TypeError("method takes one or two positional arguments, {} supplied".format(len(args)))
    def set_row_stretch(self, *args, layout=None):
        """
        Set row stretch for a given layout.

        Takes either two arguments ``index`` and ``stretch``, or a single list of stretches for all rows.
        """
        layout,lkind=self._sublayouts[layout or self._default_layout]
        for i,s in self._normalize_stretch(args):
            if lkind=="grid":
                layout.setRowStretch(i,s)
            elif lkind=="vbox":
                layout.setStretch(i,s)
            else:
                raise ValueError("only gird and vbox layout support column stretch")
    def set_column_stretch(self, *args, layout=None):
        """
        Set column stretch for a given layout.

        Takes either two arguments ``index`` and ``stretch``, or a single list of stretches for all columns.
        """
        layout,lkind=self._sublayouts[layout or self._default_layout]
        for i,s in self._normalize_stretch(args):
            if lkind=="grid":
                layout.setColumnStretch(i,s)
            elif lkind=="hbox":
                layout.setStretch(i,s)
            else:
                raise ValueError("only gird and hbox layout support column stretch")

    def add_decoration_label(self, text, location="next"):
        """Add a decoration text label with the given text"""
        label=QtWidgets.QLabel(self)
        label.setText(str(text))
        label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.add_to_layout(label,location)
        return label
    def insert_row(self, row, sublayout=None, stretch=0):
        """Insert a new row at the given location in the grid layout"""
        layout,kind=self._sublayouts[sublayout or self._default_layout]
        if kind!="grid":
            raise ValueError("can add rows only to grid layouts (vbox layouts work automatically)")
        utils.insert_layout_row(layout,row%(layout.rowCount() or 1),stretch=stretch)
    def insert_column(self, col, sublayout=None, stretch=0):
        """Insert a new column at the given location in the grid layout"""
        layout,kind=self._sublayouts[sublayout or self._default_layout]
        if kind!="grid":
            raise ValueError("can add columns only to grid layouts (hbox layouts work automatically)")
        utils.insert_layout_column(layout,col%(layout.colCount() or 1),stretch=stretch)

    def clear(self):
        """Clear the layout and remove all the added elements"""
        utils.clean_layout(self.main_layout,delete_layout=True)
        if self.main_layout is not None:
            self._set_main_layout()
            self._sublayouts={"main":(self.main_layout,self.main_layout_kind)}
            self._spacers=[]


class QLayoutManagedWidget(IQLayoutManagedWidget, QtWidgets.QWidget):
    """
    GUI widget which can manage layouts.

    Typically, first it is set up using :meth:`setup` method to specify the master layout kind;
    afterwards, widgets and sublayout can be added using :meth:`add_to_layout`.
    In addition, it can directly add named sublayouts using :meth:`add_sublayout` method.
    
    Simply a combination of :class:`IQLayoutManagedWidget` and ``QWidget``.
    """