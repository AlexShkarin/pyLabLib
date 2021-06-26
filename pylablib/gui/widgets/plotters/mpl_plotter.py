from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

from ....core.gui import QtWidgets

import matplotlib.pyplot as mpl
import time



class MPLFigureCanvas(FigureCanvasQTAgg):
    """
    Simple widget wrapper for MPL plotting canvas.
    """
    def __init__(self, parent=None):
        super().__init__(mpl.Figure())
        if parent:
            self.setParent(parent)
        self.redraw_period=0.01
        self._last_draw_time=None

    def redraw(self, force=False):
        """
        Replot the data.

        If ``force==False``, and less than ``self.redraw_period`` (10ms by default) passed since the last replot event, do nothing.
        """
        t=time.time()
        if force or (not self._last_draw_time) or (self._last_draw_time+self.redraw_period<=t):
            self.draw_idle()
            self._last_draw_time=t



class MPLFigureToolbarCanvas(QtWidgets.QFrame):
    """
    Simple widget wrapper for MPL plotting canvas with the toolbar (for plot zooming/panning)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout=QtWidgets.QVBoxLayout(self)
        self.canvas=MPLFigureCanvas(self)
        self.main_layout.addWidget(self.canvas)
        self.figure=self.canvas.figure
        self.toolbar=NavigationToolbar(self.canvas,self)
        self.main_layout.addWidget(self.toolbar)
    @property
    def redraw_period(self):
        """Set redraw period"""
        return self.canvas.redraw_period
    @redraw_period.setter
    def redraw_period(self, value):
        """Get redraw period"""
        self.canvas.redraw_period=value
    def redraw(self, force=False):
        """
        Replot the data.

        If ``force==False``, and less than ``self.redraw_period`` (10ms by default) passed since the last replot event, do nothing.
        """
        self.canvas.redraw(force=force)