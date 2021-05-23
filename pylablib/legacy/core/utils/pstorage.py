"""
Implements names lifting feature (works both for attributes and for methods), similar to the standard class inheritance.
The goal is solely to simplify syntax (shortcut access to parameters deep in the subarguments tree).
Multiple inclusion is allowed (e.g., A->B->C and A->D->C), but recursive containment (A->B->C->A) is not.
"""

from __future__ import print_function

from weakref import WeakSet

from . import functions

def _get_lookup_table(storage, import_table):
    """
    Compile lookup table for the given import parameters.

    Lookup table format it ``{alias: [value]}``; list here serves as reference to the variable
    """
    original_lookup_table=storage._lookup_table
    new_lookup_table=dict()
    for (name, alias) in import_table.items():
        if alias and name!="*" and (name in original_lookup_table):
            if alias is True:
                alias=name
            new_lookup_table[alias]=original_lookup_table[name]
    general_names=set(original_lookup_table).difference(import_table) #Names without specific rule
    if "*" in import_table and import_table["*"]:
        mask=import_table["*"]
        if mask==True:
            mask="*"
        for name in general_names:
            new_lookup_table[mask.replace("*",name)]=original_lookup_table[name]
    return new_lookup_table
            

class ParametersStorage(object):
    """
    The basic class that stores local parameters and references to other (imported) storages.
    """
    def __init__(self):
        object.__init__(self)
        object.__setattr__(self,"_lookup_table",{})
        object.__setattr__(self,"_local_table",{}) # to implement re-importing of storages
        self._imported_storages=[]
        self._containing_storages=WeakSet()
            
    def _add_local_parameter(self, name, value):
        """
        Add a new local parameter to this object.
        """
        val=[value,self]
        self._local_table[name]=val
        self._lookup_table[name]=val
        self._notify_importers()
    def _del_local_parameter(self, name):
        """
        Delete a local parameter belonging to this object.
        """
        del self._local_table[name]
        del self._lookup_table[name]
        self._notify_importers()
        
    def _get_name_dest(self, name):
        """
        Get the final destination of the given name.

        Return tuple ``(storage, name)``, where the name is given within the storage.
        For a complex name (with possible ``'.'`` or ``'/'`` separators) get the leaf storage and name.
        The leaf storage may also be a generic container (names can be transformed into integers if possible in that case).
        Will raise :exc:`KeyError` if the storage doesn't exist.
        """
        name=name.replace("/",".")
        if name.find(".")!=-1:
            names=name.split(".")
            for n in names[:-1]:
                self=self._lookup_table[n][0]
            name=names[-1]
        return (self,name)
    def _get_parameter(self, name):
        """
        Get the parameter value, taking into account imported storages.
        """
        try:
            self,name=self._get_name_dest(name)
            param=self._lookup_table[name][0]
            if hasattr(param,"__get__"): # work with descriptors
                return param.__get__(self,type(self))
            return param
        except KeyError:
            raise AttributeError("'{0}' object has no parameter '{1}'".format(self.__class__.__name__,name))
        
    def _set_parameter(self, name, value):
        """
        Set the parameter value, taking into account imported storages.
        """
        try:
            self,name=self._get_name_dest(name)
            param=self._lookup_table[name][0]
            if hasattr(param,"__set__"): # work with descriptors
                param.__set__(self,value)
            else:
                self._lookup_table[name][0]=value
            return True
        except KeyError:
            return False
        
    
    def _import_storage(self, storage, import_table=None):
        """
        Add another storage, using import parameters defined by `import_table`.
    
        `import_table` is a dictionary of the type ``{name: alias}`` ;
        if alias evaluates to ``False``, the name is not imported; if alias is ``True``, the name of the parameter is preserved; otherwise alias is used to access this parameter
        the special name "*" provides default behavior (if alias for this name contains "*" symbol, it will be replaced with a name for any specific variable)
        """
        if import_table is None:
            import_table={"*": True}
        self._lookup_table.update( _get_lookup_table(storage,import_table) )
        self._imported_storages.append((storage,import_table))
        storage._containing_storages.add(self)
        self._notify_importers()
    def _remove_storage(self, storage):
        """
        Remove the storage from the imported storages list and update the parameters list.
        """
        storage._containing_storages.remove(self)
        self._imported_storages=[(st,it) for (st,it) in self._imported_storages if not (st is storage._lookup_table)]
        self._reimport_storages()
        self._notify_importers()
    def _get_owning_storage(self, name):
        try:
            return self._lookup_table[name][1]
        except KeyError:
            raise AttributeError("'{0}' object has no parameter '{1}'".format(self.__class__.__name__,name))
    def _reimport_storages(self):
        """
        Recursively update (re-imports) all of the storages without recursively updating them.
        """
        self._lookup_table=self._local_table.copy()
        for storage,import_table in self._imported_storages:
            self._lookup_table.update( _get_lookup_table(storage,import_table) )
    def _build_notification_order(self, current, visited, order):
        """
        Arrange all of the containers containing this storage in an ordered list (containing storages coming before contained storages). 
        """
        visited.add(self)
        current.add(self)
        for importer in self._containing_storages:
            if importer in current:
                raise RuntimeError("recursive referencing is found in pstorage structure")
            if not (importer in visited):
                order=importer._build_notification_order(current,visited,order)
        current.remove(self)
        order.append(self)
        return order
    def _notify_importers(self):
        """
        Update all the of storages importing this storage (directly or indirectly).
        """
        notification_order=self._build_notification_order(current=set(),visited=set(),order=[])[:-1] # last element is self
        for importer in notification_order:
            importer._reimport_storages()
            


class ParametersStorageInterface(ParametersStorage):
    """
    An interface of the :class:`ParametersStorage`.

    Lets access parameters as if they were attributes or container items, and implements ``__dir__`` method for autocomplete.
    By default, the attribute interface (``s.p=0``) adds a usual attribute, while the container interface (``s["p"]=0``) adds a new local parameter.
    """
    def __init__(self):
        ParametersStorage.__init__(self)
    
    def __setattr__(self, name, value):
        if (name in self.__dict__) or (not ParametersStorage._set_parameter(self, name, value)):
            #self.__dict__[name]=value
            object.__setattr__(self,name,value)
    __getattr__=ParametersStorage._get_parameter
    
    def __setitem__(self, name, value):
        if not self._set_parameter(name, value):
            self._add_local_parameter(name, value)
    __getitem__=ParametersStorage._get_parameter
    __delitem__=ParametersStorage._del_local_parameter
    def __contains__(self, name):
        return name in self._lookup_table
    
    def descriptor_to_storage(self, desc_name, stored_name=None):
        """
        Add a descriptor (usually a property) with the name `desc_name` to the storage.

        If ``stored_name`` is not ``None``, use it as the name of the parameter inside the storage.
        """
        if stored_name is None:
            stored_name=desc_name
        self._add_local_parameter(stored_name,getattr(type(self),desc_name))
        
    def __dir__(self):
        return list(self.__dict__.keys())+list(self._lookup_table.keys())


def init(init_func):
    """
    ``__init__`` function decorator. 
    """
    @functions.getargsfrom(init_func)
    def wrapped(self, *args, **kwargs):
        ParametersStorageInterface.__init__(self)
        init_func(self,*args,**kwargs)
    return wrapped