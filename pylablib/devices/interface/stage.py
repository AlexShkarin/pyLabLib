from ...core.devio import interface
from ...core.utils import py3, general


class IStage(interface.IDevice):  # pylint: disable=abstract-method
    """Generic stage class"""
    _p_direction=interface.EnumParameterClass("direction",[("+",True),(1,True),("-",False),(0,False)])


def muxaxis(*args, argname="axis", **kwargs):
    """Multiplex the function over its axis argument"""
    if len(args)>0:
        return muxaxis(argname=argname,**kwargs)(args[0])
    def all_ax_func(self, *_, **__):
        return self._mapped_axes
    def def_ax_func(self, *_, **__):
        if self._default_axis is None:
            raise TypeError("{} argument must be provided".format(argname))
        return self._default_axis
    return general.muxcall(argname,special_args={"all":all_ax_func,None:def_ax_func},mux_argnames=kwargs.get("mux_argnames",None),return_kind=kwargs.get("return_kind","list"),allow_partial=True)
class IMultiaxisStage(IStage):  # pylint: disable=abstract-method
    """
    Generic multiaxis stage class.

    Has methods to assign and map axes and the axis device parameter.

    Args:
        default_axis: default axis parameter value used when ``axis=None`` is provided
    """
    _axes=[]
    _axis_parameter_name="axis"
    _axis_value_case=None
    def __init__(self, *args, default_axis="all", **kwargs):
        super().__init__(*args,**kwargs)
        self._original_axis_parameter=None
        self._default_axis=default_axis
        self._mapped_axes=list(self._axes)
        self._add_parameter_class(interface.EnumParameterClass(self._axis_parameter_name,self._axes,value_case=self._axis_value_case))
        self._add_info_variable("axes",self.get_all_axes)
    def get_all_axes(self):
        """Get the list of all available axes (taking mapping into account)"""
        return list(self._mapped_axes)
    def _update_axes(self, axes):
        """Update axes list; also removes the axes mapping"""
        self._axes=axes
        self._mapped_axes=axes
        self._replace_parameter_class(interface.EnumParameterClass(self._axis_parameter_name,self._axes,value_case=self._axis_value_case))
        self._original_axis_parameter=None
    def remap_axes(self, mapping, accept_original=True):
        """
        Rename axes to the new labels.

        `mapping` is the new axes mapping, which can be a list of new axes name (corresponding to the old axes in order returned by :meth:`get_all_axes`),
        or a dictionary ``{alias: original}`` of the new axes aliases.
        """
        if isinstance(mapping,py3.textstring):
            mapping=list(mapping)
            if len(mapping)!=len(self._axes):
                raise ValueError("number of mapped axes {} is different from the number of the original axes {}".format(mapping,self._axes))
        if isinstance(mapping,(list,tuple)):
            mapping=dict(zip(mapping,self._axes))
        opar=self._original_axis_parameter
        if opar is None:
            self._original_axis_parameter=opar=self._parameters[self._axis_parameter_name]
        wpar=interface.EnumParameterClass(self._axis_parameter_name,mapping,allowed_alias=("device_values" if accept_original else "exact"))
        self._mapped_axes=[wpar.i(ax) for ax in self._axes]
        self._replace_parameter_class(interface.CombinedParameterClass(self._axis_parameter_name,[wpar,opar]))