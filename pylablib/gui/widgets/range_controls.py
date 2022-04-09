from ...core.gui import QtCore, QtWidgets, Signal

from ...core.gui.widgets.param_table import ParamTable
from ...core.utils.numerical import limit_to_range
from ...core.utils import funcargparse

import collections




##### Range control #####

class RangeCtl(QtWidgets.QWidget):
    """
    Class for range control.

    Can have any subset of 3 rows: specifying min-max, specifying center-span (connected to min-max), and specifying step.

    Like most complex widgets, requires calling :meth:`setup` to set up before usage.

    Args:
        parent: parent widget

    Signals:
        - ``value_changed``: emitted when the value is changed
    """
    def setup(self, lim=(None,None), order=True, formatter=".1f", labels=("Min","Max","Center","Span","Step"), elements=("minmax","cspan","step")):
        """
        Setup the range control.

        Args:
            lim (tuple): limit containing min and max values
            order (bool): if ``True``, first value is always smaller than the second one (values are swapped otherwise)
            formatter (str): formatter for all edit boxes; see :func:`.format.as_formatter` for details
            labels (tuple): tuple of 5 labels for 5 controls: min, max, center, span, and step (need to always specify 5, even if no all elements are included)
            elements (tuple): tuple specifying elements which are displayed for the control;
                can contain ``"minmax"`` (min-max row), ``"cspan"`` (center-span row), and ``"step"`` (step row)
        """
        self.order=order
        self.rng=(0,0,0) if "step" in elements else (0,0)
        self.main_layout=QtWidgets.QGridLayout(self)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setContentsMargins(0,0,0,0)
        self.params=ParamTable(self)
        self.main_layout.addWidget(self.params)
        self.params.setup(name="params",add_indicator=False,change_focused_control=True)
        self.params.main_layout.setContentsMargins(5,5,5,5)
        self.params.main_layout.setSpacing(4)
        if "minmax" in elements:
            self.params.add_num_edit("min",formatter=formatter,label=labels[0])
            self.params.add_num_edit("max",formatter=formatter,label=labels[1],location=(-1,2))
            self.params.vs["min"].connect(self._minmax_changed)
            self.params.vs["max"].connect(self._minmax_changed)
        if "cspan" in elements:
            self.params.add_num_edit("cent",formatter=formatter,label=labels[2])
            self.params.add_num_edit("span",formatter=formatter,label=labels[3],location=(-1,2))
            self.params.vs["cent"].connect(self._cspan_changed)
            self.params.vs["span"].connect(self._cspan_changed)
        if "step" in elements:
            self.params.add_num_edit("step",formatter=formatter,limiter=(0,None),label=labels[4])
            self.params.vs["step"].connect(self._step_changed)
        self.params.set_column_stretch([0,1,0,1])
        self._show_values(self.rng)
        self.set_limit(lim)

    def _limit_range(self, rng):
        vmin=limit_to_range(rng[0],*self.lim)
        vmax=limit_to_range(rng[1],*self.lim)
        if self.order:
            vmin,vmax=min(vmin,vmax),max(vmin,vmax)
        if "step" in self.params:
            step=max(0,rng[2]) if len(rng)>2 else 0
            return (vmin,vmax,step)
        else:
            return (vmin,vmax)
    def _minmax_changed(self):
        rng=(self.params.v["min"],self.params.v["max"])+self.rng[2:]
        self.set_value(rng)
    def _cspan_changed(self):
        cent,span=self.params.v["cent"],self.params.v["span"]
        rng=((cent-span/2.),(cent+span/2.))+self.rng[2:]
        self.set_value(rng)
    def _step_changed(self):
        rng=self.rng[0],self.rng[1],self.params.v["step"]
        self.set_value(rng)

    def set_limit(self, lim):
        """Set range values limit (2-tuple)"""
        self.lim=lim
        self.set_value(self.rng)

    value_changed=Signal(object)
    def get_value(self):
        """Get current range value (3-tuple ``(left, right, step)`` if step is included, or 2-tuple ``(left, right)`` if it's not)"""
        return self.rng
    def _show_values(self, rng):
        if "min" in self.params:
            self.params.w["min"].set_value(rng[0],notify_value_change=False)
            self.params.w["max"].set_value(rng[1],notify_value_change=False)
        if "cent" in self.params:
            self.params.w["cent"].set_value((rng[0]+rng[1])/2.,notify_value_change=False)
            self.params.w["span"].set_value(rng[1]-rng[0],notify_value_change=False)
        if "step" in self.params:
            self.params.w["step"].set_value(rng[2],notify_value_change=False)
    def set_value(self, rng, notify_value_change=True):
        """
        Get current range value
        
        `rng` is a 2-tuple ``(left, right)``
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        """
        rng=self._limit_range(rng)
        self._show_values(rng)
        if self.rng!=rng:
            self.rng=rng
            if notify_value_change:
                self.value_changed.emit(rng)







##### ROI control #####


TAxisParams=collections.namedtuple("TAxisParams",["min","max"])
class ROICtl(QtWidgets.QWidget):
    """
    Class for ROI control.

    Has 2 rows (for X and Y coordinates), each with 2 numerical edits: min and max (or width, depending on :func:`setup` parameters).

    Like most complex widgets, requires calling :meth:`setup` to set up before usage.

    Args:
        parent: parent widget

    Attributes:
        value_changed: signal emitted when the ROI value is changed
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.xparams=TAxisParams(0,1)
        self.yparams=TAxisParams(0,1)
        self.validate=None
        self.xlim=(0,None)
        self.ylim=(0,None)
        self.minsize=0

    def _limit_range(self, rng, lim, minsize, maxsize):
        vmin=limit_to_range(rng.min,*lim)
        vmax=limit_to_range(rng.max,*lim)
        vmin,vmax=min(vmin,vmax),max(vmin,vmax)
        if vmax-vmin<minsize: # try increase upper limit
            vmax=limit_to_range(vmin+minsize,*lim)
        if vmax-vmin<minsize: # try decrease lower limit
            vmin=limit_to_range(vmax-minsize,*lim)
        if maxsize and (vmax-vmin>minsize):
            vmax=vmin+maxsize
        return TAxisParams(int(vmin),int(vmax))
    def validateROI(self, xparams, yparams):
        """Restrict current ROI values according to the class constraints"""
        xminsize,yminsize=self.minsize if isinstance(self.minsize,tuple) else (self.minsize,self.minsize)
        xmaxsize,ymaxsize=self.maxsize if isinstance(self.maxsize,tuple) else (self.maxsize,self.maxsize)
        xparams=self._limit_range(xparams,self.xlim,xminsize,xmaxsize)
        yparams=self._limit_range(yparams,self.ylim,yminsize,ymaxsize)
        if self.validate:
            xparams,yparams=self.validate((xparams,yparams))
            xparams=TAxisParams(*xparams)
            yparams=TAxisParams(*yparams)
        return xparams,yparams
    def setup(self, xlim=(0,None), ylim=None, minsize=0, maxsize=None, labels=("X","Y"), kind="minmax", validate=None):
        """
        Setup the ROI control.

        Args:
            xlim (tuple): limit for x-axis min and max values
            ylim (tuple): limit for y-axis min and max values
            sizelim (int or tuple): minimal allowed size (int implies same for both axes)
            maxsize (int or tuple): maximal allowed size (int implies same for both axes)
            kind (str): can be ``"minmax"`` (each axis control are min, max, and bin), ``"minsize"`` (each axis control are min, size and bin),
                or ``"centersize"`` (each axis control are center, size and bin)
            validate: if not ``None``, a function which takes tuple ``(xparams, yparams)`` of two axes parameters (each is a 3-tuple ``(min, max, bin)``)
                and return their constrained versions.
        """
        funcargparse.check_parameter_range(kind,"kind",["minmax","minsize","centersize"])
        self.kind=kind
        self.setMinimumSize(QtCore.QSize(110,70))
        self.setMaximumSize(QtCore.QSize(2**16,60))
        self.main_layout=QtWidgets.QVBoxLayout(self)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setContentsMargins(0,0,0,0)
        self.params=ParamTable(self)
        self.main_layout.addWidget(self.params)
        self.params.setup(name="params",add_indicator=False)
        self.params.main_layout.setContentsMargins(5,5,5,5)
        self.params.main_layout.setSpacing(4)
        self.params.add_decoration_label("ROI",(0,0))
        self.params.add_decoration_label("Center" if kind=="centersize" else "Min",(0,1))
        self.params.add_decoration_label("Max" if kind=="minmax" else "Size",(0,2))
        self.params.add_decoration_label(labels[0],(1,0))
        self.params.add_decoration_label(labels[1],(2,0))
        self.params.add_num_edit("x_min",value=0,formatter="int",limiter=(None,None,"coerce","int"),location=(1,1,1,1))
        self.params.add_num_edit("x_max",value=1,formatter="int",limiter=(None,None,"coerce","int"),location=(1,2,1,1))
        self.params.add_num_edit("y_min",value=0,formatter="int",limiter=(None,None,"coerce","int"),location=(2,1,1,1))
        self.params.add_num_edit("y_max",value=1,formatter="int",limiter=(None,None,"coerce","int"),location=(2,2,1,1))
        self.params.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Preferred))
        self.params.set_column_stretch([0,1,1])
        self.validate=validate
        for n in ["x_min","x_max","y_min","y_max"]:
            self.params.w[n].setMinimumWidth(30)
            self.params.vs[n].connect(self._on_edit)
        self.set_limits(xlim,ylim,minsize=minsize,maxsize=maxsize)


    def set_limits(self, xlim="keep", ylim="keep", minsize="keep", maxsize="keep"):
        """
        Set limits for various parameters.

        If value is ``"keep"``, keep the current value; if value is ``None``, impose no constraints.
        `maxbin`, `minsize` and `maxsize` can be integers or 2-tuples depending on whether the limits are the same or different for two axes.
        """
        if xlim!="keep":
            self.xlim=xlim
        if ylim!="keep":
            self.ylim=ylim or xlim
        if minsize!="keep":
            self.minsize=minsize
        if maxsize!="keep":
            self.maxsize=maxsize
        for n in ["x_min","x_max"]:
            self.params.w[n].set_limiter((self.xlim[0],self.xlim[1],"coerce","int"))
        for n in ["y_min","y_max"]:
            self.params.w[n].set_limiter((self.ylim[0],self.ylim[1],"coerce","int"))
        self._show_values(*self.get_value())

    value_changed=Signal(object)
    def _on_edit(self):
        params=self.get_value()
        self._show_values(*params)
        self.value_changed.emit(params)

    def get_value(self):
        """
        Get ROI value.

        Return tuple ``(xparams, yparams)`` of two axes parameters (each is a 2-tuple ``(min, max)``).
        """
        if self.kind=="minmax":
            xparams=TAxisParams(self.params.v["x_min"],self.params.v["x_max"])
            yparams=TAxisParams(self.params.v["y_min"],self.params.v["y_max"])
        elif self.kind=="minsize":
            xmin=self.params.v["x_min"]
            ymin=self.params.v["y_min"]
            xparams=TAxisParams(xmin,xmin+self.params.v["x_max"])
            yparams=TAxisParams(ymin,ymin+self.params.v["y_max"])
        elif self.kind=="centersize":
            xmin=int(self.params.v["x_min"]-self.params.v["x_max"]/2)
            ymin=int(self.params.v["y_min"]-self.params.v["y_max"]/2)
            xparams=TAxisParams(xmin,xmin+self.params.v["x_max"])
            yparams=TAxisParams(ymin,ymin+self.params.v["y_max"])
        return self.validateROI(xparams,yparams)
    def _show_values(self, xparams, yparams):
        if self.kind=="minmax":
            xmin,ymin=xparams.min,yparams.min
            xmax,ymax=xparams.max,yparams.max
        elif self.kind=="minsize":
            xmin,ymin=xparams.min,yparams.min
            xmax,ymax=xparams.max-xparams.min,yparams.max-yparams.min
        elif self.kind=="centersize":
            xmin,ymin=(xparams.max+xparams.min+1)//2,(yparams.max+yparams.min+1)//2
            xmax,ymax=xparams.max-xparams.min,yparams.max-yparams.min
        self.params.w["x_min"].set_value(xmin,notify_value_change=False)
        self.params.w["x_max"].set_value(xmax,notify_value_change=False)
        self.params.w["y_min"].set_value(ymin,notify_value_change=False)
        self.params.w["y_max"].set_value(ymax,notify_value_change=False)
    def set_value(self, roi, notify_value_change=True):
        """
        Set ROI value.

        `roi` is a tuple ``(xparams, yparams)`` of two axes parameters (each is a 2-tuple ``(min, max)``).
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        """
        roi=TAxisParams(*roi[0]),TAxisParams(*roi[1])
        params=self.validateROI(*roi)
        self._show_values(*params)
        if notify_value_change:
            self.value_changed.emit(params)




TBinAxisParams=collections.namedtuple("TBinAxisParams",["min","max","bin"])
class BinROICtl(QtWidgets.QWidget):
    """
    Class for ROI control with binning.

    Has 2 rows (for X and Y coordinates), each with 3 numerical edits: min, max (or width, depending on :func:`setup` parameters), and bin.

    Like most complex widgets, requires calling :meth:`setup` to set up before usage.

    Args:
        parent: parent widget

    Attributes:
        value_changed: signal emitted when the ROI value is changed
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.xparams=TBinAxisParams(0,1,1)
        self.yparams=TBinAxisParams(0,1,1)
        self.validate=None
        self.xlim=(0,None)
        self.ylim=(0,None)
        self.minsize=0
        self.maxbin=None

    def _limit_range(self, rng, lim, maxbin, minsize, maxsize):
        vmin=limit_to_range(rng.min,*lim)
        vmax=limit_to_range(rng.max,*lim)
        vmin,vmax=min(vmin,vmax),max(vmin,vmax)
        if vmax-vmin<minsize: # try increase upper limit
            vmax=limit_to_range(vmin+minsize,*lim)
        if vmax-vmin<minsize: # try decrease lower limit
            vmin=limit_to_range(vmax-minsize,*lim)
        if maxsize and (vmax-vmin>minsize):
            vmax=vmin+maxsize
        vbin=limit_to_range(rng.bin,1,maxbin)
        return TBinAxisParams(int(vmin),int(vmax),int(vbin))
    def validateROI(self, xparams, yparams):
        """Restrict current ROI values according to the class constraints"""
        xminsize,yminsize=self.minsize if isinstance(self.minsize,tuple) else (self.minsize,self.minsize)
        xmaxsize,ymaxsize=self.maxsize if isinstance(self.maxsize,tuple) else (self.maxsize,self.maxsize)
        xparams=self._limit_range(xparams,self.xlim,self.maxbin,xminsize,xmaxsize)
        yparams=self._limit_range(yparams,self.ylim,self.maxbin,yminsize,ymaxsize)
        if self.validate:
            xparams,yparams=self.validate((xparams,yparams))
            xparams=TBinAxisParams(*xparams)
            yparams=TBinAxisParams(*yparams)
        return xparams,yparams
    def setup(self, xlim=(0,None), ylim=None, maxbin=None, minsize=0, maxsize=None, labels=("X","Y"), kind="minmax", validate=None):
        """
        Setup the ROI control.

        Args:
            xlim (tuple): limit for x-axis min and max values
            ylim (tuple): limit for y-axis min and max values
            maxbin (int or tuple): maximal allowed binning (int implies same for both axes)
            minsize (int or tuple): minimal allowed size (int implies same for both axes)
            maxsize (int or tuple): maximal allowed size (int implies same for both axes)
            kind (str): can be ``"minmax"`` (each axis control are min, max, and bin), ``"minsize"`` (each axis control are min, size and bin),
                or ``"centersize"`` (each axis control are center, size and bin)
            validate: if not ``None``, a function which takes tuple ``(xparams, yparams)`` of two axes parameters (each is a 3-tuple ``(min, max, bin)``)
                and return their constrained versions.
        """
        funcargparse.check_parameter_range(kind,"kind",["minmax","minsize","centersize"])
        self.kind=kind
        self.setMinimumSize(QtCore.QSize(110,70))
        self.setMaximumSize(QtCore.QSize(2**16,60))
        self.main_layout=QtWidgets.QVBoxLayout(self)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setContentsMargins(0,0,0,0)
        self.params=ParamTable(self)
        self.main_layout.addWidget(self.params)
        self.params.setup(name="params",add_indicator=False)
        self.params.main_layout.setContentsMargins(5,5,5,5)
        self.params.main_layout.setSpacing(4)
        self.params.add_decoration_label("ROI",(0,0))
        self.params.add_decoration_label("Center" if kind=="centersize" else "Min",(0,1))
        self.params.add_decoration_label("Max" if kind=="minmax" else "Size",(0,2))
        self.params.add_decoration_label("Bin",(0,3))
        self.params.add_decoration_label(labels[0],(1,0))
        self.params.add_decoration_label(labels[1],(2,0))
        self.params.add_num_edit("x_min",value=0,formatter="int",limiter=(None,None,"coerce","int"),location=(1,1,1,1))
        self.params.add_num_edit("x_max",value=1,formatter="int",limiter=(None,None,"coerce","int"),location=(1,2,1,1))
        self.params.add_num_edit("x_bin",value=1,formatter="int",limiter=(None,None,"coerce","int"),location=(1,3,1,1))
        self.params.add_num_edit("y_min",value=0,formatter="int",limiter=(None,None,"coerce","int"),location=(2,1,1,1))
        self.params.add_num_edit("y_max",value=1,formatter="int",limiter=(None,None,"coerce","int"),location=(2,2,1,1))
        self.params.add_num_edit("y_bin",value=1,formatter="int",limiter=(None,None,"coerce","int"),location=(2,3,1,1))
        self.params.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Preferred))
        self.params.set_column_stretch([0,2,2,1])
        self.validate=validate
        for n in ["x_min","x_max","x_bin","y_min","y_max","y_bin"]:
            self.params.w[n].setMinimumWidth(30)
            self.params.vs[n].connect(self._on_edit)
        self.set_limits(xlim,ylim,maxbin=maxbin,minsize=minsize,maxsize=maxsize)


    def set_limits(self, xlim="keep", ylim="keep", maxbin="keep", minsize="keep", maxsize="keep"):
        """
        Set limits for various parameters.

        If value is ``"keep"``, keep the current value; if value is ``None``, impose no constraints.
        `maxbin`, `minsize` and `maxsize` can be integers or 2-tuples depending on whether the limits are the same or different for two axes.
        """
        if xlim!="keep":
            self.xlim=xlim
        if ylim!="keep":
            self.ylim=ylim or xlim
        if maxbin!="keep":
            self.maxbin=maxbin
        if minsize!="keep":
            self.minsize=minsize
        if maxsize!="keep":
            self.maxsize=maxsize
        for n in ["x_min","x_max"]:
            self.params.w[n].set_limiter((self.xlim[0],self.xlim[1],"coerce","int"))
        for n in ["y_min","y_max"]:
            self.params.w[n].set_limiter((self.ylim[0],self.ylim[1],"coerce","int"))
        for n in ["x_bin","y_bin"]:
            self.params.w[n].set_limiter((1,self.maxbin,"coerce","int"))
        self._show_values(*self.get_value())

    value_changed=Signal(object)
    def _on_edit(self):
        params=self.get_value()
        self._show_values(*params)
        self.value_changed.emit(params)

    def get_value(self):
        """
        Get ROI value.

        Return tuple ``(xparams, yparams)`` of two axes parameters (each is a 3-tuple ``(min, max, bin)``).
        """
        if self.kind=="minmax":
            xparams=TBinAxisParams(self.params.v["x_min"],self.params.v["x_max"],self.params.v["x_bin"])
            yparams=TBinAxisParams(self.params.v["y_min"],self.params.v["y_max"],self.params.v["y_bin"])
        elif self.kind=="minsize":
            xmin=self.params.v["x_min"]
            ymin=self.params.v["y_min"]
            xparams=TBinAxisParams(xmin,xmin+self.params.v["x_max"],self.params.v["x_bin"])
            yparams=TBinAxisParams(ymin,ymin+self.params.v["y_max"],self.params.v["y_bin"])
        elif self.kind=="centersize":
            xmin=int(self.params.v["x_min"]-self.params.v["x_max"]/2)
            ymin=int(self.params.v["y_min"]-self.params.v["y_max"]/2)
            xparams=TBinAxisParams(xmin,xmin+self.params.v["x_max"],self.params.v["x_bin"])
            yparams=TBinAxisParams(ymin,ymin+self.params.v["y_max"],self.params.v["y_bin"])
        return self.validateROI(xparams,yparams)
    def _show_values(self, xparams, yparams):
        if self.kind=="minmax":
            xmin,ymin=xparams.min,yparams.min
            xmax,ymax=xparams.max,yparams.max
        elif self.kind=="minsize":
            xmin,ymin=xparams.min,yparams.min
            xmax,ymax=xparams.max-xparams.min,yparams.max-yparams.min
        elif self.kind=="centersize":
            xmin,ymin=(xparams.max+xparams.min+1)//2,(yparams.max+yparams.min+1)//2
            xmax,ymax=xparams.max-xparams.min,yparams.max-yparams.min
        self.params.w["x_min"].set_value(xmin,notify_value_change=False)
        self.params.w["x_max"].set_value(xmax,notify_value_change=False)
        self.params.w["x_bin"].set_value(xparams.bin,notify_value_change=False)
        self.params.w["y_min"].set_value(ymin,notify_value_change=False)
        self.params.w["y_max"].set_value(ymax,notify_value_change=False)
        self.params.w["y_bin"].set_value(yparams.bin,notify_value_change=False)
    def set_value(self, roi, notify_value_change=True):
        """
        Set ROI value.

        `roi` is a tuple ``(xparams, yparams)`` of two axes parameters (each is a 3-tuple ``(min, max, bin)``).
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        """
        roi=TBinAxisParams(*roi[0]),TBinAxisParams(*roi[1])
        params=self.validateROI(*roi)
        self._show_values(*params)
        if notify_value_change:
            self.value_changed.emit(params)