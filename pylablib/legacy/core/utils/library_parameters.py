"""Storage for global library parameters"""

from . import dictionary, module as module_utils

class LibraryParametersStorage(object):
    """
    Global library parameters storage.

    Args:
        root_name(str): name of the root module

    On creation goes through the root module and all of its submodules and checks if any have ``'_module_parameters'`` variable.
    If they do, this variable is interpreted as a dictionary with parameters from that module.
    All of the found dictionaries are stored together and the contained parameters can be transparently read and changed.
    """
    def __init__(self, root_name):
        object.__init__(self)
        self.root_name=root_name
        self.parameters=self._collect_parameters(self.root_name)
    
    @staticmethod
    def _collect_parameters(pkg_name):
        all_packages=module_utils.get_loaded_package_modules(pkg_name)
        values={}
        for name,pkg in all_packages.items():
            if hasattr(pkg,"_module_parameters"):
                values[name]=pkg._module_parameters
        return values

    def refresh(self):
        """Repeat the modules scan (should be called if any of the modules are reloaded)"""
        self.parameters=self._collect_parameters(self.root_name)
    
    def __getitem__(self, name):
        res=dictionary.Dictionary()
        for v in self.parameters.values():
            res.update(v)
        return res[name]
    def __setitem__(self, name, value):
        name="/".join(dictionary.normalize_path(name))
        for v in self.parameters.values():
            if name in v:
                v[name]=value
                return
        raise KeyError("can't find parameter named {}".format(name))
    def __str__(self):
        return str(self[""].as_dict("flat"))
    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,str(self))

    def update(self, d):
        """Update parameters with the supplied dictionary"""
        for k,v in d.items():
            self[k]=v