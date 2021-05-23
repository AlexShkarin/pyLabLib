from ..utils import files as file_utils #@UnresolvedImport

import os
import datetime


class DataFile(object):
    """
    Describes a single datafile.
    
    Args:
        data: The main data of the file (usually :class:`.DataTable` or :class:`.Dictionary`).
        filepath (str): absolute path
        filetype (str): a source type
        creation_time (datetime.datetime): File creation time
        props (dict): all the metainfo about the file (extracted from comments, filename etc.)
        comments (list): all the comments excluding the ones containing props
    """
    def __init__(self, data, filepath=None, filetype=None, creation_time=None, comments=None, props=None):
        object.__init__(self)
        self.data=data
        if filepath is not None:
            filepath=os.path.abspath(filepath)
            self.filename=os.path.basename(filepath)
        else:
            self.filename=None
        self.filepath=filepath
        self.filetype=filetype
        if creation_time is None:
            if filepath is not None:
                creation_time=file_utils.get_file_modification_time(filepath,timestamp=False)
            else:
                creation_time=datetime.datetime.now()
        self.creation_time=creation_time
        self.comments=comments or []
        self.props=props or {}
    
    def addprop(self, name, value):
        """
        Add a property to the dictionary
        """
        self.props[name]=value
        
    def getprop(self, name, default=None):
        """
        Get a property from the dictionary. Use default value if it's not found
        """
        return self.props.get(name,default)