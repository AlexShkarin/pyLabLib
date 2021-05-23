import sip

def delete_layout_item(layout, idx):
    """Remove and item with the given index (completely delete it)"""
    if layout:
        item=layout.takeAt(idx)
        layout.removeItem(item)
        if item.layout():
            clean_layout(item.layout())
        if item.widget():
            clean_layout(item.widget().layout())
            item.widget().deleteLater()
def clean_layout(layout, delete_layout=False):
    """
    Delete all items from the layout.

    If ``delete_layout==True``, delete the layout as well.
    """
    if layout:
        while layout.count():
            delete_layout_item(layout,0)
        if delete_layout:
            sip.delete(layout)


def is_layout_row_empty(layout, row):
    """Check if the given row in a grid layout is empty"""
    if layout:
        if row<layout.rowCount():
            return False
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
def insert_layout_row(layout, row):
    """
    Insert row in a grid layout at a given tow index.

    Any multi-column item spanning over the row (i.e., starting at least one row before `row` and ending at least on row after `row`) gets stretched.
    Anything else either stays in place (if it's above `row`), or gets moved one row down.
    """
    if layout:
        free_row=get_first_empty_row(layout,row+1)
        items_to_shift=[]
        for i in range(layout.count()):
            pos=layout.getItemPosition(i)
            if pos[0]<free_row and pos[0]+pos[2]>row:
                items_to_shift.append((layout.itemAt(i),pos))
        for i,_ in items_to_shift:
            layout.removeItem(i)
        for i,p in items_to_shift:
            row_shift=1 if p[0]>=row else 0
            layout.addItem(i,p[0]+row_shift,p[1],p[2]+(1-row_shift),p[3])

def compress_grid_layout(layout):
    """Find all empty rows in a grid layout and shift them to the bottom"""
    if layout:
        curr_row=0
        filled_rows=layout.rowCount()
        while curr_row<filled_rows:
            if is_layout_row_empty(layout,curr_row):
                items_to_shift=[]
                for i in range(layout.count()):
                    pos=layout.getItemPosition(i)
                    if pos[0]>curr_row:
                        items_to_shift.append((layout.itemAt(i),pos))
                for i,_ in items_to_shift:
                    layout.removeItem(i)
                for i,p in items_to_shift:
                    layout.addItem(i,p[0]-1,p[1],p[2],p[3])
                filled_rows-=1
            else:
                curr_row+=1