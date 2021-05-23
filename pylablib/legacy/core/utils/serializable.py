"""
Mixing class for converting object into dict structure.
If an attribute of an object is also serializable, it is going to be added to the top level of the dict.
Avoid recursive attributes (``x.a=y; y.b=x``), since they will lead to errors while trying to load an object.
Avoid recursive containers (``x[0]=y; y[0]=x``), since they will lead to an infinite loop while serializing.
Choice of the attributes to serialize is the same for all objects of the same class
"""

from future.utils import viewitems, viewvalues
from .py3 import textstring

import inspect
from . import string

class Serializable(object):
    """
    A serializable object: can be converted to/from a dictionary structure.
    """
    _classes={}
    @staticmethod
    def _find_class(name, case_sensitive=True):
        """
        Find the class name in the list of registered classes (can be case insensitive).

        Raise error if the class isn't found.
        """
        try:
            _,cls=string.find_dict_string(name,Serializable._classes,case_sensitive=case_sensitive)
            return cls
        except KeyError:
            raise KeyError("can't find serializable class: {0}".format(name))
    @classmethod
    def _register_class(cls, name=None, attributes=None):
        """
        To be called after class definition to register it in the main class list. 
        """
        if name is None:
            name=cls.__name__
        cls._class_name=name
        cls._objects_count=0
        Serializable._classes[name]=cls
        if attributes is None:
            attributes={}
        attributes.setdefault("init","auto")
        if attributes["init"]=="auto": # derive from __init__ function
            attributes["init"]=inspect.getargspec(cls.__init__).args[1:] # first argument is self, last argument is name
            if len(attributes["init"])>0 and attributes["init"][-1]=="name": # last argument is name
                attributes["init"]=attributes["init"][:-1]
        attributes.setdefault("attr",[])
        cls._serializable_attributes=attributes
    @classmethod
    def _find_attribute_name(cls, name, case_sensitive=True):
        """
        Find the attribute name in the attribute list (can be case insensitive).abs
        
        Return tuple ``(name, type)``, where type can be ``'init'`` (attribute is passed to the constructor) or ``'attr'`` (attribute is assigned later).
        Raise error if attribute isn't found.
        """
        for attr_type in ["init","attr"]:
            try:
                name=string.find_list_string(name,cls._serializable_attributes[attr_type],case_sensitive=case_sensitive)[1]
                return name,attr_type
            except KeyError:
                pass
        raise KeyError("can't find attribute {0} for class {1}".format(name,cls._class_name)) 
    @classmethod
    def _new_object_name(cls):
        """
        Generate a new unique object name using the shared counter.
        """
        name="{0}_{1}".format(cls._class_name,cls._objects_count)
        cls._objects_count=cls._objects_count+1
        return name
    
    def __init__(self, name=None):
        object.__init__(self)
        if not hasattr(self,"_object_name"):
            if name is None:
                name=self.__class__._new_object_name()
            self._object_name=name
    
    def _get_init_parameter(self, name):
        """
        Get the ``'init'`` parameter with the given name.

        Can be overloaded if init parameter isn't stored plainly in the object.
        If parameter doesn't need to be saved, raise :exc:`AttributeError`.
        """
        return getattr(self,name)
    def _get_attr_parameter(self, name):
        """
        Get the ``'attr'`` parameter with the given name.

        Can be overloaded if attr parameter isn't stored plainly in the object.
        If parameter doesn't need to be saved, raise :exc:`AttributeError`.
        """
        return getattr(self,name)
    def _set_attr_parameter(self, name, value):
        """
        Set the ``'attr'`` parameter with the given name.

        Can be overloaded if attr parameter setting isn't just equivalent to the value assignment.
        """
        setattr(self,name,value)
    
    def _serialize(self, full_dict):
        """
        Add the object into the dictionary `full_dict` and return the corresponding dict key (its name).
        """
        name=self._object_name
        if name in full_dict:
            return name #already serialized (or at least started)
        obj_dict=full_dict[name]={"__type__":self.__class__._class_name}
        for attr_name in self._serializable_attributes["init"]:
            try:
                attr=self._get_init_parameter(attr_name)
                obj_dict[attr_name]=_serialize(attr,full_dict)
            except AttributeError:
                pass
        for attr_name in self._serializable_attributes["attr"]:
            try:
                attr=self._get_attr_parameter(attr_name)
                obj_dict[attr_name]=_serialize(attr,full_dict)
            except AttributeError:
                pass
        return name
    @staticmethod
    def _deserialize(name, full_dict, loaded, case_sensitive=True):
        """
        Load the object with the given name from the `full_dict` dictionary.

        Return the loaded object, which is also added to the `loaded` dict under the given name.
        Only the initialization (assinging ``'init'`` attributes) of the object is performed; assign additional (``'attr'``) attributes is done later.
        `case_sensitive` determines if the object name matching in `full_dict` is case insensitive.
        """
        if name in loaded["#incomplete"]:
            raise ValueError("initialization loops for object {0}".format(name))
        try:
            name,obj_dict=string.find_dict_string(name,full_dict,case_sensitive=case_sensitive)
        except KeyError:
            raise KeyError("object isn't present in the dictionary: {0}".format(name))
        if name in loaded:
            return loaded[name] # already loaded
        cls=Serializable._find_class(obj_dict["__type__"],case_sensitive=case_sensitive)
        loaded["#incomplete"].append(name)
        init_dict={}
        for attr_name in obj_dict:
            if not string.string_equal(attr_name,"__type__",case_sensitive=case_sensitive):
                exact_name,attr_type=cls._find_attribute_name(attr_name,case_sensitive=case_sensitive)
                if attr_type=="init":
                    attr_val=_deserialize(obj_dict[attr_name],full_dict,loaded,case_sensitive=case_sensitive)
                    init_dict[exact_name]=attr_val
        loaded["#incomplete"].remove(name)
        obj=cls(**init_dict)
        obj._object_name=name
        loaded[name]=obj
        return obj
    def _set_additional_attributes(self, full_dict, loaded, case_sensitive=True):
        """
        Set additional attributes to the object after it has been loaded.
        """
        name=self._object_name
        if not name in full_dict:
            return
        obj_dict=full_dict[name]
        for attr_name in obj_dict:
            if not string.string_equal(attr_name,"__type__",case_sensitive=case_sensitive):
                exact_name,attr_type=self._find_attribute_name(attr_name,case_sensitive=case_sensitive)
                if attr_type=="attr":
                    attr_val=_deserialize(obj_dict[attr_name],full_dict,loaded)
                    self._set_attr_parameter(exact_name,attr_val)
    def _string_repr(self, attr_repr="repr"):
        params=[]
        if attr_repr=="repr":
            attr_repr=repr
        else:
            attr_repr=str
        for attr_name in self._serializable_attributes["init"]:
            try:
                attr=self._get_init_parameter(attr_name)
                params.append("{0}: {1}".format(attr_name,attr_repr(attr)))
            except AttributeError:
                pass
        for attr_name in self._serializable_attributes["attr"]:
            try:
                attr=self._get_init_parameter(attr_name)
                params.append("{0}: {1}".format(attr_name,attr_repr(attr)))
            except AttributeError:
                pass
        params=", ".join(params)
        return "("+params+")"


def _serialize(obj, full_dict, deep_copy=True):
    """
    Serialize object `obj` into the dictionary.

    Return the value which is to be stored in the dictionary and later used to deserialize the object.
    If the object is :class:`Serializable`, store it on the top level of `full_dict` and return its name. Otherwise, return the object itself.
    Containeres (lists, tuples and dictionaries) are processed recursively.
    If ``deep_copy==True``, attempt to copy (call ``.copy()`` method) all non-serializable attributes before returning them.
    """
    if isinstance(obj, Serializable):
        return obj._serialize(full_dict)
    if isinstance(obj, list):
        return [_serialize(elt,full_dict) for elt in obj]
    if isinstance(obj, tuple):
        return tuple([_serialize(elt,full_dict) for elt in obj])
    if isinstance(obj, dict):
        ser_dict={}
        for k,v in viewitems(obj):
            ser_dict[k]=_serialize(v,full_dict) # assume that k doesn't contain any serializable objects
        return ser_dict
    if deep_copy:
        try:
            return obj.copy()
        except AttributeError:
            pass
    return obj
    
def _deserialize(obj, full_dict, loaded, case_sensitive, deep_copy=True):
    """
    Deserialize object `obj` from the dictionary.

    If `obj` is a string, try to interpret it as a name of a stored :class:`Serializable` object and add it into `loaded` dict;
    if this name is missing, treat it as a string value.
    Containere (lists, tuples and dictionaries) objects are processed recursively.
    If ``deep_copy==True``, attempt to copy (call ``.copy()`` method) all non-serializable attributes before returning them.
    """
    if isinstance(obj,textstring):
        if obj in full_dict:
            return Serializable._deserialize(obj,full_dict,loaded,case_sensitive=case_sensitive)
        else: # assume that value is string itself
            return obj
    if isinstance(obj,list):
        return [_deserialize(elt,full_dict,loaded,case_sensitive=case_sensitive) for elt in obj]
    if isinstance(obj,tuple):
        return tuple([_deserialize(elt,full_dict,loaded,case_sensitive=case_sensitive) for elt in obj])
    if isinstance(obj,dict):
        deser_dict={}
        for k,v in viewitems(obj):
            deser_dict[k]=_deserialize(v,full_dict,loaded,case_sensitive=case_sensitive)
        return deser_dict
    if deep_copy:
        try:
            return obj.copy()
        except AttributeError:
            pass
    return obj


def init_name(object_name_arg="name"):
    """
    ``__init__`` function decorator. 
    """
    if object_name_arg is None:
        def decorator(init_func):
            def wrapped(self, *args, **vargs):
                Serializable.__init__(self)
                init_func(self,*args,**vargs)
            return wrapped
    else:
        def decorator(init_func):
            def wrapped(self, *args, **vargs):
                Serializable.__init__(self,vargs.get(object_name_arg,None))
                if object_name_arg in vargs:
                    del vargs[object_name_arg]
                init_func(self,*args,**vargs)
            return wrapped
    return decorator
init=init_name()


def to_dict(objects, full_dict=None, deep_copy=True):
    """
    Serialize the list of objects into the dictionary.

    Return `full_dict`.
    If ``deep_copy==True``, attempt to copy (call ``.copy()`` method) all non-serializable attributes before storing them in the dictionary.
    Only :class:`Serializable` objects get serialized.
    """
    if full_dict is None:
        full_dict={}
    if isinstance(objects,Serializable):
        objects=[objects]
    for obj in objects:
        _serialize(obj,full_dict,deep_copy=deep_copy)
    return full_dict
def from_dict(full_dict, case_sensitive=True, deep_copy=True):
    """
    Deserialize objects from the dictionary.

    Return a dictionary ``{name: object}`` containing the extracted objects.
    If ``deep_copy==True``, attempt to copy (call ``.copy()`` method) all non-serializable attributes before assigning them as objects attributes.
    Only :class:`Serializable` objects get deserialized.
    """
    loaded={"#incomplete":[]} #contains list of object currently being created, to escape recursive loops
    for name in full_dict:
        _deserialize(name,full_dict,loaded,case_sensitive=case_sensitive)
    del loaded["#incomplete"]
    for obj in viewvalues(loaded):
        obj._set_additional_attributes(full_dict,loaded,case_sensitive=case_sensitive)
    return loaded