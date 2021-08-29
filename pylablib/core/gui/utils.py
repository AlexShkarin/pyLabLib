from . import qdelete

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