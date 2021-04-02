from ...core.devio import interface

class IStage(interface.IDevice):
    _axis_parameter_name="axis"
    def __init__(self):
        super().__init__()
        self._original_axis_parameter=None
    def remap_axes(self, mapping, accept_original=True):
        if isinstance(mapping,(list,tuple)):
            mapping=dict((v,i) for (i,v) in enumerate(mapping))
        opar=self._original_axis_parameter
        if opar is None:
            self._original_axis_parameter=opar=self._parameters[self._axis_parameter_name]
        wpar=interface.EnumParameterClass(self._axis_parameter_name,mapping,alias_case=None,allowed_alias=("all" if accept_original else "exact"),match_prefix=False)
        self._replace_parameter_class(interface.CombinedParameterClass(self._axis_parameter_name,[wpar,opar]))