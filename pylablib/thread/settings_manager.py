from ..core.thread import controller
from ..core.utils import dictionary


class SettingsManager(controller.QTaskThread):
    """
    Settings manager.
    
    Keeps track of all the settings sources (each settings source can add more of them),
    usually in order to save them when the data is being saved.
    """
    def setup_task(self):  # pylint: disable=arguments-differ
        self.sources={}
        self.values={}
        self.add_command("add_source")
        self.add_command("add_thread_variable_source")
        self.add_command("add_value")
        self.add_command("get_all_settings")

    def add_source(self, name, func):
        """Add settings source as a function (called in the settings thread when settings values are requested)"""
        self.sources[name]=func
    def add_thread_variable_source(self, name, thread, variable):
        def get_value():
            ctl=controller.sync_controller(thread)
            return ctl[variable]
        self.add_source(name,get_value)
    def add_value(self, name, settings):
        """Add settings values directly"""
        self.values[name]=settings
    
    def get_all_settings(self, include=None, exclude=None, alias=None):
        """
        Get all settings values
        
        If `include` is not ``None``, it specifies a list of setting sources to include (by default, all sources).
        If `exclude` is not ``None``, it specifies a list of setting sources to exclude (by default, none are excluded).
        If `alias` is not ``None``, specifies aliases (i.e., different names in the resulting dictionary) for settings nodes.
        """
        settings=dictionary.Dictionary()
        alias=alias or {}
        for s in self.sources:
            if ((include is None) or (s in include)) and ((exclude is None) or (s not in exclude)):
                sett=self.sources[s]()
                settings.update({alias.get(s,s):sett})
        for s in self.values:
            if ((include is None) or (s in include)) and ((exclude is None) or (s not in exclude)) and (s not in settings):
                sett=self.values[s]
                settings.update({alias.get(s,s):sett})
        return settings