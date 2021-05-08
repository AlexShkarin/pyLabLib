from ..utils import files as file_utils

import os
import datetime


class DataFile:
    """
    Describes a single datafile.
    
    Args:
        data: the main content of the file (usually a numpy array, a pandas DataFrame or a :class:`.Dictionary`).
        filepath (str): absolute path from which the file was read
        filetype (str): a source type (e.g., ``"csv"`` or ``"bin"``)
        creation_time (datetime.datetime): File creation time
        props (dict): all the metainfo about the file (extracted from comments, filename etc.)
        comments (list): all the comments excluding the ones containing props
    """
    def __init__(self, data, filepath=None, filetype=None, creation_time=None, comments=None, props=None):
        self.data=data
        if filepath is not None:
            self.filepath=os.path.abspath(filepath)
            self.filename=os.path.basename(filepath)
        else:
            self.filepath=None
            self.filename=None
        self.filetype=filetype
        if creation_time is None:
            if filepath is not None:
                creation_time=file_utils.get_file_modification_time(filepath,timestamp=False)
            else:
                creation_time=datetime.datetime.now()
        self.creation_time=creation_time
        self.comments=comments or []
        self.props=props or {}

    def __getitem__(self, name):
        return self.props[name]
    def __setitem__(self, name, value):
        self.props[name]=value
    def get(self, name, default=None):
        """Get a property from the dictionary. Use default value if it's not found"""
        return self.props.get(name,default)