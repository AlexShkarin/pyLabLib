from ...core.gui import QtWidgets, QtCore, utils, is_pyqt5
from ...core.utils import funcargparse


class QPlaceAnchor(QtWidgets.QWidget):
    """
    Place anchor widget.

    Invisible and does not (in most cases) affect the layout.
    Serves as an additional "anchor point" for the highlighter,
    usually to mark a given cell in a gird layout.
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setMinimumSize(0,0)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred))
        self.resize(0,0)
    def sizeHint(self):
        return QtCore.QSize(0,0)
    def minimumSizeHint(self):
        return QtCore.QSize(0,0)



class QAnchorEventFilter(QtCore.QObject):
    """
    Even filter, which notifies the highlighter to update its boundaries.

    Args:
        src: event source (the one to which the filter is attached)
        dst: event destination, which get s boundaries update notification.
    """
    def __init__(self, src, dst):
        super().__init__(parent=dst)
        self.src=src
        self.dst=dst
    def eventFilter(self, watched, event):
        t=event.type()
        if t in [QtCore.QEvent.Move,QtCore.QEvent.Resize,QtCore.QEvent.Show,QtCore.QEvent.Hide]:
            if watched is self.src:
                if t==QtCore.QEvent.Move:
                    update=(watched,{"pos":event.pos()})
                elif t==QtCore.QEvent.Resize:
                    update=(watched,{"size":event.size()})
                elif t==QtCore.QEvent.Show:
                    update=(watched,{"visible":True})
                elif t==QtCore.QEvent.Hide:
                    update=(watched,{"visible":False})
            else:
                update=None
            self.dst.update_boundaries(update=update)
        return False



class QHighlightFrame(QtWidgets.QFrame):
    """
    Highlighter frame.

    A rectangle frame which takes some anchors and adjusts its position and size to cover all of them.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1,1)
        self.move(0,0)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
    
    def setup(self, border=0, style=None):
        """
        Setup the frame.

        `border` specifies the frame border, which offsets the frame from the anchor points.
        `style` set the frame stylesheet.
        """
        self.anchors=[]
        self.place_anchors=[]
        self.filters={}
        self.border=border
        self.style=style or ""
        self.setStyleSheet(self.style)
    def add_anchor(self, anchor):
        """
        Add an anchor widget.

        For proper boundary updates this widget should already be placed into its final layout place.
        """
        if anchor not in self.anchors:
            self.anchors.append(anchor)
            f=QAnchorEventFilter(anchor,self)
            parents=utils.get_all_layout_containers(anchor) or []
            for p in parents:
                p.installEventFilter(f)
            self.filters[anchor]=f,parents
            self.update_boundaries()
        return anchor
    def make_place_anchor(self, parent=None):
        """
        Make a place anchor, which can be later placed into a layout.

        Note that after placing to the layout, it should still be added using :meth:`add_anchor`.
        """
        if parent is None:
            parent=self.parent()
        anchor=QPlaceAnchor(parent)
        self.place_anchors.append(anchor)
        return anchor
    def add_layout_anchor(self, container, anchor, kind="element"):
        """
        Add an anchor related to the given container.

        `anchor` can be an anchor widget, a widget's name within the container (usually applies to parameter tables)
         or a position withing the `container` layout.
        `kind` determines the added anchor span; can be ``"element"`` (cover only this specific element),
        or ``"row"`` (cover the whole row).
        If `anchor` is not contained within `container`, then `kind` is set to ``"element"`` by default.
        """
        funcargparse.check_parameter_range(kind,"kind",["element","row"])
        if anchor is container:
            self.add_anchor(anchor)
            return
        if isinstance(anchor,str):
            try:
                anchor=container.w[anchor]
            except KeyError:
                anchor=container.c[anchor]
        if isinstance(anchor,QtWidgets.QWidget):
            container=utils.get_layout_container(anchor,top=container)
            if kind=="element" or container is None:
                self.add_anchor(anchor)
                return
            sl,loc=container.get_element_position(anchor)
        else:
            if isinstance(anchor,tuple) and anchor and isinstance(anchor[0],str) and anchor!="next":
                sl,loc=anchor[0],anchor[1:]
            else:
                sl,loc=("main",anchor)
        if not isinstance(loc,tuple):
            loc=(loc,)
        sublayout=container.get_sublayout(sl)
        if container.get_sublayout_kind(sl)=="grid":
            if kind=="element":
                add_locs=[(sl,loc)]
            else:
                loc=loc+("next",0,1,1)[len(loc):]
                add_locs=[(sl,loc[0],0), (sl,loc[0]+loc[2]-1,-1)]
            for l in add_locs:
                e=self.make_place_anchor(parent=container)
                container.add_to_layout(e,l)
                self.add_anchor(e)
        elif container.get_sublayout_kind(sl)=="vbox":
            if sublayout.count():
                e=sublayout.itemAt(loc[0]).widget()
                self.add_anchor(e)
        elif container.get_sublayout_kind(sl)=="hbox":
            n=sublayout.count()
            if kind=="element":
                if sublayout.count():
                    e=sublayout.itemAt(loc[0]).widget()
                    self.add_anchor(e)
            else:
                for i in range(n):
                    e=container.get_sublayout(sl).itemAt(i).widget()
                    if e is not None:
                        self.add_anchor(e)
                        break
                for i in range(n-1,-1,-1):
                    e=container.get_sublayout(sl).itemAt(i).widget()
                    if e is not None:
                        self.add_anchor(e)
                        break
    def remove_anchor(self, anchor, delete=True):
        """
        Remove previously added anchor.
        
        If ``remove==True`` and `anchor` is a place anchor made using :meth:`make_place_anchor`, it is automatically destroyed.
        """
        del self.anchors[self.anchors.index(anchor)]
        if anchor in self.filters:
            f,parents=self.filters.pop(anchor)
            for p in parents:
                p.removeEventFilter(f)
        if anchor in self.place_anchors and delete:
            del self.place_anchors[self.place_anchors.index(anchor)]
            utils.delete_widget(anchor)
    def update_anchor(self, anchor):
        """
        Update anchor hierarchy.

        Should only be called if `anchor` (or its containing widget) changed its layout.
        """
        self.remove_anchor(anchor,delete=False)
        self.add_anchor(anchor)
    def remove_all_anchors(self):
        """Remove all contained anchors"""
        anchors=list(self.anchors)
        for a in anchors:
            self.remove_anchor(a)
        for a in self.place_anchors:
            utils.delete_widget(a)
        self.hide()
    def update_boundaries(self, update=None):
        """
        Update frame boundaries.

        Called automatically by the added anchors whenever they move,
        so should not normally be invoked directly.
        """
        l,r,t,b=None,None,None,None
        w,v=update or (None,None)
        visible=True
        for a in self.anchors:
            pos=a.pos() if a is not w else v.get("pos",a.pos())
            pos=self.parentWidget().mapFromGlobal(a.parentWidget().mapToGlobal(pos))
            size=a.size() if a is not w else v.get("size",a.size())
            al,at=pos.x(),pos.y()
            ar,ab=pos.x()+size.width(),pos.y()+size.height()
            if l is None:
                l,r,t,b=al,ar,at,ab
            else:
                l=min(l,al)
                r=max(r,ar)
                t=min(t,at)
                b=max(b,ab)
            avis=a.isVisible() if a is not w else v.get("visible",a.isVisible())
            visible=visible and avis
        if l is not None:
            l=max(l-self.border,0)
            t=max(t-self.border,0)
            r+=self.border
            b+=self.border
            self.move(l,t)
            self.resize(r-l,b-t)
        self.setVisible(bool(self.anchors) and visible)
    def refresh(self):
        """
        Refresh the anchor.

        In some cases can help with widget occlusion.
        """
        if is_pyqt5:
            self.setVisible(not self.isVisible())
            self.setVisible(not self.isVisible())
        self.update_boundaries()
        self.parent().update()