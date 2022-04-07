from . import qdelete, QtWidgets, QtCore

import collections

def get_top_parent(widget):
    """Find the top-level parent (parent which does not have further parents)"""
    while widget is not None and widget.parent() is not None:
        widget=widget.parent()
    return widget

def find_layout_element(layout, element):
    """
    Find a layout element.

    Can be a widget, a sublayout, or a layout element
    Return item index within the layout.
    If layout is empty or item is not present, return ``None``
    """
    if layout is not None:
        for idx in range(layout.count()):
            item=layout.itemAt(idx)
            if item is element or item.widget() is element or item.layout() is element:
                return idx

def delete_layout_item(layout, idx):
    """Remove and item with the given index (completely delete it)"""
    if layout is not None:
        item=layout.takeAt(idx)
        if item.widget() is not None:
            clean_layout(item.widget().layout(),delete_layout=True)
            item.widget().deleteLater()
        elif item.layout():
            clean_layout(item.layout(),delete_layout=True)
def clean_layout(layout, delete_layout=False):
    """
    Delete all items from the layout.

    If ``delete_layout==True``, delete the layout as well.
    """
    if layout is not None:
        while layout.count():
            delete_layout_item(layout,0)
        if delete_layout:
            qdelete(layout)

def _find_contained_widget(parent, widget, result_kind="widget"):
    if parent is widget:
        return [widget] if result_kind=="widget" else []
    if parent is None:
        return None
    if isinstance(parent,QtWidgets.QWidget):
        result=_find_contained_widget(parent.layout(),widget,result_kind=result_kind)
        if result is None and isinstance(parent,QtWidgets.QTabWidget):
            for t in range(parent.count()):
                result=_find_contained_widget(parent.widget(t),widget,result_kind=result_kind)
                if result is not None:
                    break
    else:
        layout=parent
        result=None
        if layout is not None:
            for idx in range(layout.count()):
                item=layout.itemAt(idx)
                if item.widget() is not None:
                    result=_find_contained_widget(item.widget(),widget,result_kind=result_kind)
                elif item.layout() is not None:
                    result=_find_contained_widget(item.layout(),widget,result_kind=result_kind)
                if result is not None:
                    break
    if result is not None:
        parent_kind="layout" if isinstance(parent,QtWidgets.QLayout) else "widget"
        if parent_kind==result_kind:
            result.append(parent)
        return result
def get_layout_container(widget, top=None, kind="widget"):
    """
    Find a container widget or layout which contains the given widget.

    Note that the container widget does not necessarily correspond to the element parent.
    If no container could be found, return ``None``.
    If `kind` can be either ``"widget"`` (return the containing widget),
    or ``"layout"`` (return the containing layout, which is a layout or sublayout of the containing widget).

    This method works by traversing the whole layout tree, so it can be relatively slow.
    `top` can specify the top container (widget or layout) which definitely contains the given widget;
    if not specified, use the top-level parent found by :func:`get_top_parent`.
    """
    if top is None:
        top=get_top_parent(widget)
    if kind not in {"widget","layout"}:
        raise ValueError("unrecognized result kind: {}".format(kind))
    result=_find_contained_widget(top,widget,result_kind=kind)
    if result:
        return result[:2][-1] if kind=="widget" else result[0]
def get_all_layout_containers(widget, top=None, kind="widget"):
    """
    Get a list of all widgets or layouts containing the current widget.

    The list is arranged from the bottom of the hierarchy (starting from `widget`) to the `top`.
    Note that the container widget does not necessarily correspond to the element parent.
    If no containers could be found, return ``None``.
    If `kind` can be either ``"widget"`` (return the containing widgets),
    or ``"layout"`` (return the containing layouts, which are layouts or sublayouts of the containing widgets.

    This method works by traversing the whole layout tree, so it can be relatively slow.
    `top` can specify the top container (widget or layout) which definitely contains the given widget;
    if not specified, use the top-level parent found by :func:`get_top_parent`.
    """
    if top is None:
        top=get_top_parent(widget)
    if kind not in {"widget","layout"}:
        raise ValueError("unrecognized result kind: {}".format(kind))
    return _find_contained_widget(top,widget,result_kind=kind)
def delete_widget(widget):
    """Remove widget from its layout container and delete it"""
    if widget is None:
        return False
    layout=get_layout_container(widget,kind="layout")
    if layout is not None:
        idx=find_layout_element(layout,widget)
        if idx is not None:
            delete_layout_item(layout,idx)
            return True
    widget.deleteLater()
    return False
    


TWidgetLocation=collections.namedtuple("TWidgetLocation",["layout","position"])
def get_widget_location(widget, layout=None):
    """
    Get location of a widget within the given layout.

    Return tuple ``(layout, position)``, where ``layout`` is the layout object,
    and ``position`` is either a single position number (for box layouts),
    or a tuple ``(row, col, rowspan, colspan)`` for a grid layout.
    If layout is not specified, autodetect it.
    """
    if layout is None:
        layout=get_layout_container(widget,kind="layout")
    if layout is not None:
        idx=find_layout_element(layout,widget)
        if idx is not None:
            if isinstance(layout,QtWidgets.QGridLayout):
                return TWidgetLocation(layout,layout.getItemPosition(idx))
            else:
                return TWidgetLocation(layout,idx)
def place_widget_at_location(widget, location):
    """
    Insert a widget within the given layout location.

    `location` is a tuple tuple ``(layout, position)``, where ``layout`` is the layout object,
    and ``position`` is either a single position number (for box layouts),
    or a tuple ``(row, col, rowspan, colspan)`` for a grid layout.
    The tuple has the same format as returned by :func:`get_widget_location`.
    """
    if location is not None:
        layout,position=location
        if isinstance(location.layout,QtWidgets.QGridLayout):
            layout.addWidget(widget,*position)
        else:
            layout.insertWidget(position,widget)

def is_layout_row_empty(layout, row):
    """Check if the given row in a grid layout is empty"""
    if layout is not None:
        if row>=layout.rowCount():
            return True
        for c in range(layout.columnCount()):
            if layout.itemAtPosition(row,c):
                return False
        return True
    return False
def get_last_filled_row(layout, start_row=0):
    """
    Find the last non-empty row in a grid layout after `start_row` (inclusive).
    
    If all rows after (and including) `start_row` are empty, return ``None`` .
    """
    for r in range(layout.rowCount()-1,start_row-1,-1):
        if not is_layout_row_empty(layout,r):
            return r
    return None
def get_first_empty_row(layout, start_row=0):
    """Find the first completely empty row in a grid layout after `start_row` (inclusive)"""
    for r in range(start_row,layout.rowCount()):
        if is_layout_row_empty(layout,r):
            return r
    return layout.rowCount()
def insert_layout_row(layout, row, stretch=0, compress=False):
    """
    Insert row in a grid layout at a given index.

    Any multi-column item spanning over the row (i.e., starting at least one row before `row` and ending at least one row after `row`) gets stretched.
    Anything else either stays in place (if it's above `row`), or gets moved one row down.
    `stretch` determines the stretch factor of the new row.
    If ``compress==True``, try to find an empty row below the inserted position and shit it to the new row's place;
    otherwise, add a completely new row.
    """
    if layout is not None:
        free_row=get_first_empty_row(layout,row+1) if compress else layout.rowCount()
        items_to_shift=[]
        for i in range(layout.count()):
            pos=layout.getItemPosition(i)
            if pos[0]<free_row and pos[0]+pos[2]>row:
                items_to_shift.append((i,pos))
        items_to_shift=[(layout.takeAt(i),p) for (i,p) in items_to_shift[::-1]][::-1] # remove starting from the end
        for i,p in items_to_shift:
            row_shift=1 if p[0]>=row else 0
            layout.addItem(i,p[0]+row_shift,p[1],p[2]+(1-row_shift),p[3])
        for r in range(free_row,row,-1):
            layout.setRowStretch(r,layout.rowStretch(r-1))
        layout.setRowStretch(row,stretch)


def is_layout_column_empty(layout, col):
    """Check if the given column in a grid layout is empty"""
    if layout is not None:
        if col>=layout.columnCount():
            return True
        for r in range(layout.rowCount()):
            if layout.itemAtPosition(r,col):
                return False
        return True
    return False
def get_last_filled_column(layout, start_col=0):
    """
    Find the last non-empty column in a grid layout after `start_col` (inclusive).
    
    If all rows after (and including) `start_col` are empty, return ``None`` .
    """
    for c in range(layout.colCount()-1,start_col-1,-1):
        if not is_layout_column_empty(layout,c):
            return c
    return None
def get_first_empty_column(layout, start_col=0):
    """Find the first completely empty column in a grid layout after `start_col` (inclusive)"""
    for c in range(start_col,layout.colCount()):
        if is_layout_column_empty(layout,c):
            return c
    return layout.colCount()
def insert_layout_column(layout, col, stretch=0, compress=False):
    """
    Insert column in a grid layout at a given index.

    Any multi-row item spanning over the column (i.e., starting at least one column before `col` and ending at least one column after `col`) gets stretched.
    Anything else either stays in place (if it's above `col`), or gets moved one column to the right.
    `stretch` determines the stretch factor of the new column.
    If ``compress==True``, try to find an empty column below the inserted position and shit it to the new column's place;
    otherwise, add a completely new column.
    """
    if layout is not None:
        free_col=get_first_empty_column(layout,col+1) if compress else layout.colCount()
        items_to_shift=[]
        for i in range(layout.count()):
            pos=layout.getItemPosition(i)
            if pos[1]<free_col and pos[1]+pos[3]>col:
                items_to_shift.append((i,pos))
        items_to_shift=[(layout.takeAt(i),p) for (i,p) in items_to_shift[::-1]][::-1] # remove starting from the end
        for i,p in items_to_shift:
            col_shift=1 if p[0]>=col else 0
            layout.addItem(i,p[0],p[1]+col_shift,p[2],p[3]+(1-col_shift))
        for c in range(free_col,col,-1):
            layout.setColumnsStretch(c,layout.columnStretch(c-1))
        layout.setColumnsStretch(col,stretch)


def compress_grid_layout(layout):
    """Find all empty rows in a grid layout and shift them to the bottom"""
    if layout is not None:
        curr_row=0
        filled_rows=layout.rowCount()
        while curr_row<filled_rows:
            if is_layout_row_empty(layout,curr_row):
                items_to_shift=[]
                for i in range(layout.count()):
                    pos=layout.getItemPosition(i)
                    if pos[0]>curr_row:
                        items_to_shift.append((i,pos))
                items_to_shift=[(layout.takeAt(i),p) for (i,p) in items_to_shift[::-1]][::-1] # remove starting from the end
                for i,p in items_to_shift:
                    layout.addItem(i,p[0]-1,p[1],p[2],p[3])
                filled_rows-=1
            else:
                curr_row+=1


def get_relative_position(widget, origin=None):
    """Get widget's position relative to the origin (top-level parent if ``None``)"""
    if origin is None:
        origin=get_top_parent(widget)
    return origin.mapFromGlobal(widget.parentWidget().mapToGlobal(widget.pos()))

def _expand_rectangle(rect, border, bound_size=None):
    if isinstance(border,tuple):
        bx0,bx1,by0,by1=border if len(border)==4 else (border[0],border[0],border[1],border[1])
    else:
        bx0,bx1,by0,by1=(border,)*4
    x0,y0=rect.x()-bx0,rect.y()-by0
    x1,y1=rect.x()+rect.width()+bx1,rect.y()+rect.height()+by1
    if bound_size is not None:
        x0=max(x0,0)
        y0=max(y0,0)
        x1=max(min(x1,bound_size.width()),x0)
        y1=max(min(y1,bound_size.height()),y0)
    return QtCore.QRect(x0,y0,x1-x0,y1-y0)
def get_relative_rectangle(widget, origin=None, border=0, trim_border=True):
    """
    Get widget rectangle area relative to the origin (top-level parent if ``None``).

    If `border` is non-zero, it specifies a border (integer or 2-tuple) around the widget to add to the rectangle.
    If ``trim_border==True``, the resulting rectangle is trimmed to lie withing the origin area.
    Return ``QRect`` object.
    """
    if origin is None:
        origin=get_top_parent(widget)
    pos=origin.mapFromGlobal(widget.parentWidget().mapToGlobal(widget.pos()))
    rect=QtCore.QRect(pos,widget.size())
    if border:
        rect=_expand_rectangle(rect,border,bound_size=origin.size() if trim_border else None)
    return rect

def get_screenshot(window=None, rect=None, widget=None, border=0, include_titlebar=True):
    """
    Take a screenshot of a given window or a given widget.

    Either `window` or `widget` must be defined.
    If `rect` (type ``QRect``) or `widget` are defined, they specify the area to include into screenshot;
    in this case, `border` can define an additional border to add to the rectangle.
    If rectangle is not defined, then `include_titlebar` specifies whether the window titlebar is included.
    """
    if window is None and widget is None:
        raise ValueError("either window or widget must be defined")
    if window is None:
        window=get_top_parent(widget)
    try:
        screen=window.screen()
    except AttributeError:
        screen=window.windowHandle().screen()
    if widget is None and rect is None:
        pos=window.pos() if include_titlebar else window.geometry()
        size=window.frameSize() if include_titlebar else window.size()
        rect=QtCore.QRect(QtCore.QPoint(0,0),size)
        if border:
            rect=_expand_rectangle(rect,border=border,bound_size=size)
    else:
        pos=window.geometry()
        if rect is None:
            if get_top_parent(widget) is not window:
                raise ValueError("window should be a top parent of the widget")
            rect=get_relative_rectangle(widget,origin=window)
        if border:
            rect=_expand_rectangle(rect,border=border,bound_size=window.size())
    return screen.grabWindow(0,pos.x()+rect.x(),pos.y()+rect.y(),rect.width(),rect.height())