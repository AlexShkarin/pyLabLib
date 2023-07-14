"""
Tree-like multi-level dictionary with advanced indexing options.
"""

from functools import reduce, lru_cache

from . import funcargparse, general, strdump
import re
import collections
import json
import pandas as pd

def _split_path_base(path, omit_empty=True, sep=None):
    if not (isinstance(path, list) or isinstance(path, tuple)):
        path=[path]
    else:
        path=general.flatten_list(path)
    if sep is None:
        path=[e for t in path for e in str(t).split("/")]
    else:
        path=[e for t in path for e in re.split(sep,str(t))]
    if omit_empty:
        path=[p for p in path if p!=""]
    return path
_split_path_cached=lru_cache(maxsize=10**5)(_split_path_base)
def split_path(path, omit_empty=True, sep=None):
    """
    Split generic path into individual path entries.
    
    Args:
        path: Generic path. Lists and tuples (possible nested) are flattened;
            strings are split according to separators; non-strings are converted into strings first.
        omit_empty (bool): Determines if empty entries are skipped.
        sep (str): If not ``None``, defines regex for path separators; default separator is ``'/'``.
    Returns:
        list: A list of individual entries.
    """
    try:
        return _split_path_cached(path,omit_empty=omit_empty,sep=sep)
    except TypeError:
        return _split_path_base(path,omit_empty=omit_empty,sep=sep)
def normalize_path_entry(entry, case_normalization=None):
    """Normalize the case of the entry if it's not case-sensitive. Normalization is either ``None`` (no normalization, names are case-sensitive), ``'lower'`` or ``'upper'``"""
    funcargparse.check_parameter_range(case_normalization,"case_normalization",{None,"lower","upper"})
    if case_normalization=="lower":
        return entry.lower()
    elif case_normalization=="upper":
        return entry.upper()
    else:
        return entry
def normalize_path(path, omit_empty=True, case_normalization=None, sep=None, force=False):
    """
    Split and normalize generic path into individual path entries.
    
    Args:
        path: Generic path. Lists and tuples (possible nested) are flattened;
            strings are split according to separators; non-strings are converted into strings first.
        omit_empty (bool): Determines if empty entries are skipped.
        case_normalization (str): Case normalization rules; can be ``None`` (no normalization, names are case-sensitive), ``'lower'`` or ``'upper'``.
        sep (str): If not None, defines regex for path separators; default separator is ``'/'``.
        force (bool): If ``False``, treat lists as if they're already normalized.
    Returns:
        list: A list of individual normalized entries.
    """
    if isinstance(path,list) and not force:
        return path
    funcargparse.check_parameter_range(case_normalization,"case_normalization",{None,"lower","upper"})
    path=split_path(path,omit_empty,sep=sep)
    if case_normalization=="lower":
        return [p.lower() for p in path]
    elif case_normalization=="upper":
        return [p.upper() for p in path]
    else:
        return path


def is_dictionary(obj, generic=False):
    """
    Determine if the object is a dictionary.
    
    Args:
        obj: object
        generic (bool): if ``False``, passes only :class:`Dictionary` (or subclasses) objects;
            otherwise, passes any dictionary-like object.
    Returns:
        bool
    """
    return Dictionary.is_dictionary(obj,generic=generic)
def as_dictionary(obj, case_normalization=None):
    """
    Convert object into :class:`Dictionary` with the given parameters.
    
    If object is already a :class:`Dictionary` (or its subclass), return unchanged, even if its parameters are different.
    """
    return Dictionary.as_dictionary(obj,case_normalization=case_normalization)
def as_dict(obj, style="nested", copy=True):
    """
    Convert object into standard `dict` with the given parameters.
    
    If object is already a `dict`, return unchanged, even if the parameters are different.
    """
    if isinstance(obj,dict):
        return obj
    return Dictionary.as_dictionary(obj).as_dict(style=style,copy=copy)
     







class Dictionary:
    """
    Multi-level dictionary.
    
    Access is done by path (all path elements are converted into strings and concatenated to form a single string path).
    If dictionary is not case-sensitive, all inserted and accessed paths are normalized to lower or upper case.
    
    Args:
        root (dict or Dictionary): Initial value.
        case_normalization (str): Case normalization rules; can be ``None`` (no normalization, names are case-sensitive), ``'lower'`` or ``'upper'``.
        copy (bool): If ``True``, make copy of the supplied data; otherwise, just make it the root.
        
    Warning:
        If ``copy==False``, the root data is already assumed to be normalized. If it isn't, the behavior might be incorrect.
    """
    def __init__(self, root=None, case_normalization=None, copy=True):
        self._case_normalization=case_normalization
        if root is not None:
            if isinstance(root,pd.Series):
                root=dict(zip(root.index,root))
            elif isinstance(root,pd.DataFrame):
                if root.shape[1]==1:
                    root=dict(zip(root.index,root.iloc(axis=1)[0]))
                elif root.shape[1]==2:
                    root=dict(zip(root.iloc(axis=1)[0],root.iloc(axis=1)[1]))
                else:
                    raise ValueError("only accept 1- and 2-column arrays")
            root=Dictionary._get_root(root)
            if copy:
                self._data={}
                self.merge(root) # automatically normalizes source
            else:
                self._data=root
        else:
            self._data={}
        self.ptr=ItemAccessor(getter=self.branch_pointer)
    
    def _make_similar_dict(self, root=None, copy=True):
        return Dictionary(root=root,copy=copy,case_normalization=self._case_normalization)
    def _normalize_path_entry(self, entry):
        return normalize_path_entry(entry,case_normalization=self._case_normalization)
    def _normalize_path(self, path):
        return normalize_path(path,omit_empty=True,case_normalization=self._case_normalization)
    @staticmethod
    def _is_branch(v):
        return isinstance(v,dict) 
    @staticmethod
    def _get_root(source):
        if isinstance(source, Dictionary):
            return source._data
        elif Dictionary._is_branch(source):
            return source
        else:
            raise ValueError("source isn't a tree")
    @staticmethod
    def _is_empty(source):
        if isinstance(source, Dictionary):
            return not source._data
        elif Dictionary._is_branch(source):
            return not source
        else:
            return False
    @staticmethod
    def is_dictionary(obj, generic=True):
        """
        Determine if the object is a dictionary.
    
        Args:
            obj
            generic (bool): if False, passes only :class:`Dictionary` (or subclasses) objects;
                otherwise, passes any dictionary-like object.
        Returns:
            bool
        """
        if generic:
            return isinstance(obj, Dictionary) or Dictionary._is_branch(obj)
        else:
            return isinstance(obj, Dictionary)
    @staticmethod
    def as_dictionary(obj, case_normalization=None):
        """
        Convert object into :class:`Dictionary` with the given parameters.
    
        If object is already a :class:`Dictionary` (or its subclass), return unchanged, even if its parameters are different.
        """
        if isinstance(obj,DictionaryPointer):
            return Dictionary(obj,copy=False)
        if isinstance(obj, Dictionary):
            return obj
        else:
            return Dictionary(obj,case_normalization=case_normalization)
    
    def _get_valid_subpath(self, s_path):
        branch=self._data
        i=0
        for i,p in enumerate(s_path):
            if self._is_branch(branch) and p in branch:
                branch=branch[p]
            else:
                break
        return s_path[:i]
    
    def _get_branch(self, s_path, append=False, overwrite_leaves=False):
        branch=self._data
        for p in s_path:
            if append:
                new_branch=branch.setdefault(p,{})
                if not self._is_branch(new_branch):
                    if overwrite_leaves:
                        new_branch=branch[p]={}
                    else:
                        return None
                branch=new_branch
            elif p in branch:
                branch=branch[p]
                if not self._is_branch(branch):
                    return None
            else:
                return None
        return branch

    def _attach_node(self, dest, key, value, branch_option="normalize"):
        """
        Attach a node.
        
        `branch_option` decides what to do if the value is dictionary-like: just attach root, copy, or normalize all the keys
        attaching empty dictionary does nothing.
        """
        try:
            value=Dictionary._get_root(value)
            if value: # adding empty dictionary doesn't change anything
                if branch_option=="attach":
                    dest[key]=value
                else:
                    branch={}
                    self._insert_branch(value,branch,overwrite=True,normalize_paths=(branch_option=="normalize"))
                    dest[key]=branch
        except ValueError:
            dest[key]=value
    def _clear_root(self, keep_dict=True):
        if keep_dict:
            for k in list(self._data):
                del self._data[k]
        else:
            self._data={}
    def _replace_root(self, value, branch_option="normalize", keep_dict=True):
        try:
            value=Dictionary._get_root(value)
        except ValueError:
            raise ValueError("can't replace root with a leaf")
        if value: # adding empty dictionary doesn't change anything
            if branch_option=="attach" and not keep_dict:
                self._data=value
            else:
                self._clear_root(keep_dict=keep_dict)
                self._insert_branch(value,self._data,normalize_paths=(branch_option=="normalize"))
        else:
            self._clear_root(keep_dict=keep_dict)
        
    
    def add_entry(self, path, value, force=False, branch_option="normalize"):
        """
        Add value to a given path (overwrite leaf value if necessary).
        
        Doesn't replace leaves with branches and vice-verse if ``force==False``.
        
        Args:
            path
            value
            force (bool): If ``True``, change leaf into a branch and vice-versa; otherwise, raises :exc:`ValueError` if the conversion is necessary.
            branch_option (str):
                Decides what to do if the value is dictionary-like:
                    - ``'attach'`` -- just attach the root,
                    - ``'copy'`` -- copy and attach,
                    - ``'normalize'`` -- copy while normalizing all the keys according to the current rules.
        """
        funcargparse.check_parameter_range(branch_option,"branch_option",{"attach","copy","normalize"})
        path=self._normalize_path(path)
        if path==[]:  # replacing/removing the root
            self._replace_root(value,branch_option=branch_option)
            return self
        if self._is_empty(value):
            if force:
                self.del_entry(path)
            return self
        if force:
            branch=self._get_branch(path[:-1],append=True,overwrite_leaves=True)
        else:
            branch=self._get_branch(path[:-1],append=True,overwrite_leaves=False)
            if branch is None:
                wrong_path="/".join(self._get_valid_subpath(path))
                raise KeyError("can't replace the leaf '{0}' with a subtree; delete the leaf explicitly first, or use force=True".format(wrong_path))
            if self._is_branch(branch.get(path[-1],None)):
                wrong_path="/".join(path)
                raise KeyError("can't replace the subtree '{0}' with a leaf; delete the subtree explicitly first, or use force=True".format(wrong_path))
        self._attach_node(branch,path[-1],value,branch_option=branch_option)
        return self
    def _get_entry(self, path):
        path=self._normalize_path(path)
        if path==[]:
            return self._data
        branch=self._get_branch(path[:-1],append=False)
        if branch and (path[-1] in branch):
            return branch[path[-1]]
        else:
            raise KeyError("unaccessible entry with path {0}".format(path))
    def get_entry(self, path, as_pointer=False):
        """
        Get entry at a given path
        
        Args:
            path
            as_pointer (bool): If ``True`` and entry is not a leaf, return :class:`DictionaryPointer`; otherwise, return :class:`Dictionary`
        """
        value=self._get_entry(path)
        if self._is_branch(value):
            if as_pointer:
                return DictionaryPointer(self,path,case_normalization=self._case_normalization,copy=False)
            else:
                return self._make_similar_dict(value,copy=False)
        else:
            return value
    def has_entry(self, path, kind="all"):
        """
        Determine if the path is in the dictionary.
        
        `kind` determines which kind of path to consider and can be ``'leaf'``, ``'branch'`` or ``'all'``.
        """
        funcargparse.check_parameter_range(kind,"kind",{"leaf","branch","all"})
        try:
            v=self._get_entry(path)
            return (kind=="all") or (kind=="branch" and self._is_branch(v)) or (kind=="leaf" and not self._is_branch(v))
        except KeyError:
            return False
    def is_leaf_path(self, path):
        """Determine if the path is in the dictionary and points to a leaf"""
        return self.has_entry(path,kind="leaf")
    def is_branch_path(self, path):
        """Determine if the path is in the dictionary and points to a branch"""
        return self.has_entry(path,kind="branch")
    def get_max_prefix(self, path, kind="all"):
        """
        Find the longest prefix of `path` contained in the dictionary.

        Return tuple ``(prefix, rest)``, where both path entries are normalized according to the dictionary rules (i.e., these are lists representing normalized paths).
        `kind` determines which kind of path to consider and can be ``'leaf'``, ``'branch'`` or ``'all'``. If the longest prefix is of a different kind, return ``(None,None)``.
        """
        funcargparse.check_parameter_range(kind,"kind",{"leaf","branch","all"})
        s_path=self._normalize_path(path)
        if s_path==[]:
            if not self._data and kind!="branch":
                return ([],[])
            if self._data and kind!="leaf":
                return ([],[])
            return (None,None)
        branch=self._data
        for i,p in enumerate(s_path):
            if p in branch:
                branch=branch[p]
                if not self._is_branch(branch):
                    return (None,None) if kind=="branch" else (s_path[:i+1],s_path[i+1:])
            else:
                return (None,None) if kind=="leaf" else (s_path[:i],s_path[i:])
        return (None,None) if kind=="leaf" else (s_path,[])
    def del_entry(self, path):
        """
        Delete entry from the dictionary.
        
        Return ``True`` if the path was present.
        Note that it never raises `KeyError`.
        """
        path=self._normalize_path(path)
        if path==[]:
            return False
        branch=self._get_branch(path[:-1],append=False)
        if branch:
            try:
                del branch[path[-1]]
                return True
            except KeyError:
                pass
        return False
    
    __getitem__=get_entry
    __setitem__=add_entry
    __contains__=has_entry
    __delitem__=del_entry
    def __len__(self): return len(self._data)
    def size(self):
        """Return the total size of the dictionary (number of nodes)"""
        def _branch_size(branch):
            if self._is_branch(branch):
                return sum(_branch_size(v) for v in branch.values())
            else:
                return 1
        return _branch_size(self._data)
    def get(self, path, default=None):
        """Analog of ``dict.get()``: ``D.get(k,d) -> D[k] if k in D else d``"""
        try:
            return self.__getitem__(path)
        except KeyError:
            return default
    def pop(self, path, default=None):
        """
        Analog of ``dict.pop()``: remove value at `path` and return it if ``path in D``, otherwise return `default`

        Note that it never raises :exc:`KeyError`.
        """
        try:
            return self.detach(path)
        except KeyError:
            return default

    def setdefault(self, path, default=None):
        """
        Analog of ``dict.setdefault()``: ``D.setdefault(k,d) -> D.get(k,d)``, also sets ``D[k]=d`` if ``k not in D``.
        """
        try:
            return self.__getitem__(path)
        except KeyError:
            self.__setitem__(path, default)
            return default
    def items(self, ordered=False, leafs=False, path_kind="split", wrap_branches=True):
        """
        Analog of ``dict.items()``, by default iterating only over the immediate children of the root.
        
        Args:
            ordered (bool): If ``True``, loop over keys in alphabetic order.
            leafs (bool): If ``True``, loop over leaf nodes (i.e., behave as 'flat' dictionary);
                otherwise, loop over immediate children (i.e., behave as 'nested' dictionary)
            path_kind (str): either ``"split"`` (each path is a tuple of individual keys), or ``"joined"`` (each path is a single string)
            wrap_branches (bool): if ``True``, wrap sub-branches into :class:`DictionaryPointer` objects; otherwise, return them as nested built-in dictionaries
        """
        if leafs:
            funcargparse.check_parameter_range(path_kind,"path_kind",{"split","joined"})
            makep=tuple if path_kind=="split" else "/".join
            for p,v in self.iternodes(to_visit="leafs",ordered=ordered,include_path=True):
                yield makep(p),v
        else:
            items_=sorted(self._data.items()) if ordered else self._data.items()
            if wrap_branches:
                makev=lambda p,v: (self._fast_build_branch_pointer([p],v) if self._is_branch(v) else v)
            else:
                makev=lambda p,v: v
            for p,v in items_:
                yield p,makev(p,v)
    iteritems=items # for compatibility
    viewitems=items # for compatibility
    def values(self, ordered=False, leafs=False, wrap_branches=True):
        """
        Analog of ``dict.values()``, iterating only over the immediate children of the root.

        Args:
            ordered (bool): If ``True``, loop over keys in alphabetic order.
            leafs (bool): If ``True``, loop over leaf nodes (i.e., behave as 'flat' dictionary);
                otherwise, loop over immediate children (i.e., behave as 'nested' dictionary)
            wrap_branches (bool): if ``True``, wrap sub-branches into :class:`DictionaryPointer` objects; otherwise, return them as nested built-in dictionaries
        """
        for _,v in self.items(ordered=ordered,leafs=leafs,wrap_branches=wrap_branches):
            yield v
    viewvalues=values
    itervalues=values
    def keys(self, ordered=False, leafs=False, path_kind="split"):
        """
        Analog of ``dict.keys()``, iterating only over the immediate children of the root.
        
        Args:
            ordered (bool): If ``True``, loop over keys in alphabetic order.
            leafs (bool): If ``True``, loop over leaf nodes (i.e., behave as 'flat' dictionary);
                otherwise, loop over immediate children (i.e., behave as 'nested' dictionary)
            path_kind (str): either ``"split"`` (each path is a tuple of individual keys), or ``"joined"`` (each path is a single string)
        """
        if leafs:
            for k,_ in self.items(ordered=ordered,path_kind=path_kind):
                yield k
        else:
            ks=sorted(self._data) if ordered else list(self._data)
            for k in ks:
                yield k
    viewkeys=keys # for compatibility
    iterkeys=keys # for compatibility
    def __iter__(self):
        return self._data.__iter__()
    def paths(self, ordered=False, topdown=False, path_kind="split"):
        """
        Return list of all paths (leafs and nodes).
        
        Args:
            ordered (bool): If ``True``, loop over paths in alphabetic order.
            topdown (bool): If ``True``, return node's leafs before its subtrees leafs.
            path_kind (str): either ``"split"`` (each path is a tuple of individual keys), or ``"joined"`` (each path is a single string)
        """
        ps=[]
        funcargparse.check_parameter_range(path_kind,"path_kind",{"split","joined"})
        makep=tuple if path_kind=="split" else "/".join
        for p,_ in self.iternodes(to_visit="leafs",ordered=ordered,topdown=topdown,include_path=True):
            ps.append(makep(p))
        return ps
    def _iterbranches(self, ordered=False, topdown=False):
        if topdown:
            yield self
        source=self._data
        path=self.get_path()
        iter_range=sorted(source.items()) if ordered else source.items()
        for k,v in iter_range:
            if self._is_branch(v):
                ptr=self._fast_build_branch_pointer(path+[k],v)
                for b in ptr._iterbranches(ordered=ordered,topdown=topdown):
                    yield b
        if not topdown:
            yield self
    def iternodes(self, to_visit="leafs", ordered=False, include_path=False, topdown=False):
        """
        Iterate over nodes.
        
        Args:
            to_visit (str): Can be ``'leafs'``, ``'branches'`` or ``'all'`` and determines which parts of the dictionary are visited.
            ordered (bool): If ``True``, loop over paths in alphabetic order.
            include_path (bool): Include in the return value.
            topdown (bool): If ``True``, visit node and its leafs before its subtrees leafs.
            
        Yield:
            Values for leafs and :class:`DictionaryPointer` for branches.
            If ``include_path==True``, yields tuple ``(path, value)``, where `path` is in the form of a normalized list.
        """
        funcargparse.check_parameter_range(to_visit,"to_visit",{"branches","leafs","all"})
        for br in self._iterbranches(ordered=ordered,topdown=topdown):
            path=br.get_path()
            if topdown and (to_visit in {"branches","all"}):
                yield (path,br) if include_path else br
            if to_visit in {"leafs","all"}:
                for k,v in br.items(ordered=ordered,wrap_branches=False):
                    if not self._is_branch(v):
                        yield (path+[k],v) if include_path else v
            if (not topdown) and (to_visit in {"branches","all"}):
                yield (path,br) if include_path else br
    nodes=iternodes
    
                
    def __str__(self):
        iterleafs=self.iternodes(ordered=True,to_visit="leafs",include_path=True)
        content="\n".join("'{0}': {1}".format("/".join(k),str(v)) for k,v in iterleafs)
        return "{0}({1})".format(type(self).__name__,content)
    __repr__=__str__
    
    def _insert_branch(self, source, dest, overwrite=True, normalize_paths=True):
        for k,v in source.items():
            if normalize_paths:
                k=self._normalize_path(k)
                if len(k)>1:
                    v=reduce((lambda d,sk: {sk:d}), [v]+k[:0:-1]) # build dict corresponding to {"k[1]/k[2]/.../k[-1]":v}
                k=k[0]
            else:
                k=self._normalize_path_entry(str(k))
            try:
                v=self._get_root(v)
                is_branch=True
            except ValueError:
                is_branch=False
            if is_branch:
                if k in dest and not (self._is_branch(dest[k])):
                    if overwrite:
                        dest[k]={}
                    else:
                        continue
                dest.setdefault(k,{})
                self._insert_branch(v,dest[k],overwrite=overwrite,normalize_paths=normalize_paths)
            else:
                if overwrite:
                    dest[k]=v
                else:
                    dest.setdefault(k,v)
    def merge(self, source, path="", overwrite=True, normalize_paths=True):
        """
        Attach source (:class:`dict` or other :class:`Dictionary`) to a given branch; source is automatically deep-copied.

        If `source` is not a dictionary, simply assign it (i.e., ``D.merge(v,p)`` is equivalent to ``D.add_entry(p,v,force=True)`` in this case).
        Compared to :meth:`add_entry`, merges two branches instead of removing the old branch completely.
        
        Args:
            source (dict or Dictionary)
            branch (tuple or str): Destination path.
            overwrite (bool): If ``True``, replaces the old entries with the new ones (it only matters for leaf assignments).
            normalize_paths (bool): If ``True`` and the dictionary isn't case sensitive, perform normalization if the `source`.
        """
        try:
            source=Dictionary._get_root(source)
        except ValueError:
            if overwrite or path not in self:
                self.add_entry(path,source,force=True)
            return self
        if not source:
            return self
        path=self._normalize_path(path)
        dest=self._get_branch(path,append=True,overwrite_leaves=overwrite)
        if dest is None:
            raise KeyError("can't replace the leaf '{0}' with a subtree; delete the leaf explicitly first, or use force=True".format("/".join(path)))
        self._insert_branch(source,dest,overwrite=overwrite,normalize_paths=normalize_paths)
        return self
    update=merge
    def detach(self, path):
        """
        Remove a branch or a leaf from the current dictionary.
        
        Branch is returned as a separate :class:`Dictionary`.
        If `path` is missing, raise a :exc:`KeyError`.
        """
        subtree=self[path]
        del self[path]
        return subtree
    def collect(self, paths, detach=False, ignore_missing=True):
        """
        Collect a set of subpaths into a separate dictionary.

        Args:
            paths: list or set of paths
            detach: if ``True``, added branches are removed from this dictionary
            ignore_missing: if ``True``, ignore paths from the list which are not present in this dictionary; otherwise, raise a :exc:`KeyError`.
        """
        result=self._make_similar_dict()
        for p in paths:
            try:
                v=self.detach(p) if detach else self[p]
                result[p]=v
            except KeyError:
                if not ignore_missing:
                    raise
        return result
        
    @staticmethod
    def _deep_copy(leaf):
        if Dictionary._is_branch(leaf):
            res={}
            for k,v in leaf.items():
                res[k]=Dictionary._deep_copy(v)
        else:
            res=leaf
        return res
    def branch_copy(self, branch=""):
        """Get a copy of the branch as a :class:`Dictionary`"""
        source=self._get_branch(self._normalize_path(branch),append=False)
        if source is None:
            raise KeyError("unaccessible entry with path {0}".format(branch))
        return self._make_similar_dict(self._deep_copy(source),copy=False)
    def copy(self):
        """Get a full copy the dictionary"""
        return self.branch_copy()
    def updated(self, source, path="", overwrite=True, normalize_paths=True):
        """
        Get a copy of the dictionary and attach a new branch to it.
        
        Parameters are the same as in the :meth:`Dictionary.merge`. 
        """
        cpy=self.copy()
        cpy.merge(source,path=path,overwrite=overwrite,normalize_paths=normalize_paths)
        return cpy
    def as_dict(self, style="nested", copy=True):
        """
        Convert into a :class:`dict` object.
        
        Args:
            style (str):
                Determines style of the result:
                    - ``'nested'`` -- subtrees are turned into nested dictionaries,
                    - ``'flat'`` --  single dictionary is formed with full paths as keys.
            copy (bool): If ``False`` and ``style=='nested'``, return the root dictionary. 
        """
        if isinstance(self,dict):
            return self.copy() if copy else self
        funcargparse.check_parameter_range(style,"style",{"nested","flat"})
        if style=="nested":
            return self.copy()._data if copy else self._data
        else:
            d={}
            for p,v in self.iternodes(to_visit="leafs",include_path=True):
                d["/".join(p)]=v
            return d
    asdict=as_dict  # alias to agree with the standard conventions
    def as_json(self, style="nested"):
        """
        Convert into a JSON string.

        Args:
            style (str): Determines style of the result:
                    - ``'nested'`` -- subtrees are turned into nested dictionaries,
                    - ``'flat'`` --  single dictionary is formed with full paths as keys.
        """
        return json.dumps(self.as_dict(style=style))
    @classmethod
    def from_json(cls, data, case_normalization=None):
        """Convert JSON representations of a dictionary into a :class:`Dictionary` object"""
        return cls(json.loads(data),copy=False,case_normalization=case_normalization)
    def as_pandas(self, index_key=True, as_series=True):
        """
        Convert into a pandas DataFrame or Series object.
        
        Args:
            index_key (bool): If ``False``, create a 2-column table with the first column (``"key"``) containing string path
                and the second column (``"value"``) containing value; otherwise, move key to the table index.
            as_series (bool): If ``index_key==True`` and ``as_series==True``, convert the resulting DataFrame into 1D Series
                (the key is the index); otherwise, keep it as a single-column table
        """
        data=[("/".join(p), v) for p,v in self.iternodes(to_visit="leafs",include_path=True,ordered=True)]
        table=pd.DataFrame(data,columns=["key","value"])
        if index_key:
            table=table.set_index("key")
            if as_series:
                table=table["value"]
        return table
    def __eq__(self, other):
        if isinstance(other,dict):
            return self._data==other
        if isinstance(other,type(self)):
            return self._data==other._data and self._case_normalization==other._case_normalization
        return False
    
    def get_path(self): return [] # for compatibility with pointer
    def branch_pointer(self, branch=""):
        """Get a :class:`DictionaryPointer` of a given branch"""
        return DictionaryPointer(self,branch,case_normalization=self._case_normalization,copy=False)
    def _fast_build_branch_pointer(self, norm_path, node):
        return DictionaryPointer._fast_build(self,norm_path,node,case_normalization=self._case_normalization,copy=False)
    
    
    def _map_root(self, func, pass_path, branch_option):
        ptr=self._fast_build_branch_pointer([],self._data)
        res=func(ptr.get_path(),ptr) if pass_path else func(ptr)
        if res is not ptr:
            self._replace_root(res,branch_option=branch_option)
    def map_self(self, func, to_visit="leafs", pass_path=False, topdown=False, branch_option="normalize"):
        """
        Apply `func` to the nodes in the dictionary.
        
        Note that any pointers to the replaced branches or their sub-branches will become invalid.

        Args:
            func (callable): Mapping function. Leafs are passed by value, branches (if visited) are passed as :class:`DictionaryPointer`.
            to_visit (str): Can be ``'leafs'``, ``'branches'`` or ``'all'`` and determines which parts of the dictionary passed to the map function.
            pass_path (bool): If ``True``, pass the node path (in the form of a normalized list) as a first argument to `func`.
            topdown (bool): If ``True``, visit node and its leafs before its subtrees leafs.
            branch_option (str): If the function returns a dict-like object, determines how to incorporate into the dictionary;
                can be ``"normalize"`` (make a copy with normalized paths and insert that), ``"copy"`` (make a copy without normalization),
                or ``"attach"`` (simply replace the value without copying and normalization)
        """
        funcargparse.check_parameter_range(to_visit,"to_visit",{"branches","leafs","all"})
        funcargparse.check_parameter_range(branch_option,"branch_option",{"attach","copy","normalize"})
        visit_branches=to_visit in {"branches","all"}
        visit_leafs=to_visit in {"leafs","all"}
        if topdown and visit_branches:
            self._map_root(func,pass_path,branch_option)
        for br in self._iterbranches(topdown=topdown):
            path=br.get_path()
            source=br._data
            for k,v in source.items():
                if self._is_branch(v):
                    if visit_branches:
                        ptr=self._fast_build_branch_pointer(path+[k],v)
                        res=func(ptr.get_path(),ptr) if pass_path else func(ptr)
                        if res is not ptr:
                            self._attach_node(source,k,res,branch_option=branch_option)
                elif visit_leafs:
                    res=func(path+[k],v) if pass_path else func(v)
                    if res is not v:
                        self._attach_node(source,k,res,branch_option=branch_option)
        if not topdown and visit_branches:
            self._map_root(func,pass_path,branch_option)
        return self
    def filter_self(self, pred, to_visit="leafs", pass_path=False, topdown=False):
        """
        Remove all the nodes from the dictionary for which `pred` returns ``False``.
        
        Args:
            pred (callable): Filter function. Leafs are passed to `pred` by value, branches (if visited) are passed as :class:`DictionaryPointer`.
            to_visit (str): Can be ``'leafs'``, ``'branches'`` or ``'all'`` and determines which parts of the dictionary passed to the predicate.
            pass_path (bool): If ``True``, pass the node path (in the form of a normalized list) as a first argument to `pred`.
            topdown (bool): If ``True``, visit node and its leafs before its subtrees leafs.
        """
        funcargparse.check_parameter_range(to_visit,"to_visit",{"branches","leafs","all"})
        visit_branches=to_visit in {"branches","all"}
        visit_leafs=to_visit in {"leafs","all"}
        for br in self._iterbranches(topdown=topdown):
            path=br.get_path()
            source=br._data
            for k,v in list(source.items()):
                keep=True
                if self._is_branch(v):
                    if visit_branches:
                        ptr=self._fast_build_branch_pointer(path+[k],v)
                        keep=pred(ptr.get_path(),ptr) if pass_path else pred(ptr)
                elif visit_leafs:
                    keep=pred(path+[k],v) if pass_path else pred(v)
                if not keep:
                    del source[k]
        return self
    
    
    def diff(self, other):
        """
        Perform an element-wise comparison to another Dictionary.
        
        If the other Dictionary has a different case sensitivity, raise :exc:`ValueError`.
        
        Returns:
            :class:`DictionaryDiff`
        """
        other=as_dictionary(other,case_normalization=self._case_normalization)
        if self._case_normalization!=other._case_normalization:
            raise ValueError("can't compare dictionaries with different case normalization")
        self_paths=set(["/".join(p) for p in self.paths()])
        other_paths=set(["/".join(p) for p in other.paths()])
        same_paths=set.intersection(self_paths,other_paths)
        added=self._make_similar_dict()
        removed=self._make_similar_dict()
        for p in set.difference(self_paths,same_paths):
            removed[p]=self[p]
        for p in set.difference(other_paths,same_paths):
            added[p]=other[p]
        same=self._make_similar_dict()
        changed_from=self._make_similar_dict()
        changed_to=self._make_similar_dict()
        for p in same_paths:
            vs,vo=self[p],other[p]
            if vs==vo:
                same[p]=vs
            else:
                changed_from[p]=vs
                changed_to[p]=vo
        return DictionaryDiff(same,changed_from,changed_to,removed,added)
    @staticmethod
    def diff_flatdict(first, second):
        """
        Find the difference between flat :class:`dict` objects.
        
        Returns:
            :class:`DictionaryDiff`
        """
        first_paths=set(first)
        second_paths=set(second)
        same_paths=first_paths&second_paths
        added=dict([ (k,second[k]) for k in (second_paths-same_paths) ])
        removed=dict([ (k,first[k]) for k in (first_paths-same_paths) ])
        same={}
        changed_from={}
        changed_to={}
        for p in same_paths:
            vf,vs=first[p],second[p]
            if vf==vs:
                same[p]=vf
            else:
                changed_from[p]=vf
                changed_to[p]=vs
        return DictionaryDiff(same,changed_from,changed_to,removed,added)
    @staticmethod
    def find_intersection(dicts, use_flatten=False):
        """
        Find intersection of multiple dictionaries.
        
        Args:
            dicts ([:class:`Dictionary`])
            use_flatten (bool): If ``True`` flatten all dictionaries before comparison (works faster for a large number of dictionaries).
        
        Returns:
            :class:`DictionaryIntersection`
        """
        if len(dicts)==0:
            return DictionaryIntersection(Dictionary(),[])
        if len(dicts)==1:
            return DictionaryIntersection(dicts[0],[Dictionary()])
        if not use_flatten:
            common=dicts[0]
            for d in dicts[1:]:
                common=common.diff(d).same
            individual=[d.diff(common).removed for d in dicts]
            return DictionaryIntersection(common,individual)
        else:
            d0=dicts[0]
            for d in dicts[1:]:
                if d._case_normalization!=d0._case_normalization:
                    raise ValueError("can't intersect dictionaries with different case normalization")
            fdicts=[d.as_dict("flat") for d in dicts]
            common=fdicts[0]
            for d in fdicts[1:]:
                common=Dictionary.diff_flatdict(common,d).same
            individual=[Dictionary.diff_flatdict(d,common).removed for d in fdicts]
            common=d0._make_similar_dict(common)
            individual=[d0._make_similar_dict(i) for i in individual]
            return DictionaryIntersection(common,individual)

    def _add_dict(self, d1, d2):
        if self._is_branch(d1):
            for k,v in d2.items():
                if k in d1:
                    self._add_dict(d1[k],v)
                else:
                    d1[k]=v
    def _dfs_pattern(self, path, root, wildkey, wildpath, match_leaves, wrap_nodes=None):
        if wrap_nodes is None:
            wrap_nodes=not match_leaves
        res=(root,) if wrap_nodes else root
        if not path:
            return res, not (match_leaves and self._is_branch(root))
        if not self._is_branch(root):
            return res, (len(path)==1 and path[0]==wildpath)
        if path[0]==wildkey:
            res={}
            for k,v in root.items():
                mv,succ=self._dfs_pattern(path[1:],v,wildkey,wildpath,match_leaves,wrap_nodes=wrap_nodes)
                if succ:
                    res[k]=mv
            return res,bool(res)
        elif path[0]==wildpath:
            mvd,succd=self._dfs_pattern(path[1:],root,wildkey,wildpath,match_leaves,wrap_nodes=wrap_nodes)
            mvk={}
            for k,v in root.items():
                mv,succ=self._dfs_pattern(path,v,wildkey,wildpath,match_leaves,wrap_nodes=wrap_nodes)
                if succ:
                    mvk[k]=mv
            if succd:
                if mvk:
                    self._add_dict(mvd,mvk)
                return mvd,True
            else:
                return mvk,bool(mvk)
        elif path[0] in root:
            mv,succ=self._dfs_pattern(path[1:],root[path[0]],wildkey,wildpath,match_leaves,wrap_nodes=wrap_nodes)
            return ({path[0]:mv} if succ else None), succ
        else:
            return None,False
                    
    def get_matching_paths(self, pattern, wildkey="*", wildpath="**", only_leaves=True):
        """
        Get all paths in the tree that match the provided pattern.
        
        Args:
            wildkey (str): Pattern symbol that matches any key.
            wildpath (str): Pattern symbol that matches any subpath (possibly empty).
            only_leaves (bool): If ``True``, only check leaf paths; otherwise, check subtree paths (i.e., incomplete leaf paths) as well.
                Basically, ``only_leaves=False`` is analogous to adding wildpath at the end of the pattern.
        """
        s_path=self._normalize_path(pattern)
        dfs_tree,matched=self._dfs_pattern(s_path,self._data,wildkey,wildpath,match_leaves=only_leaves)
        if not matched:
            return []
        def _get_paths(d):
            if self._is_branch(d):
                return [ [k]+p for (k,v) in d.items() for p in _get_paths(v)]
            else:
                return [[]]
        paths=_get_paths(dfs_tree)
        return paths
    def get_matching_subtree(self, pattern, wildkey="*", wildpath="**", only_leaves=True):
        """
        Get a subtree containing nodes with paths matching the provided pattern.
        
        Args:
            wildkey (str): Pattern symbol that matches any key.
            wildpath (str): Pattern symbol that matches any subpath (possibly empty).
            only_leaves (bool): If ``True``, only check leaf paths; otherwise, check subtree paths (i.e., incomplete leaf paths) as well.
                Basically, ``only_leaves=False`` is analogous to adding wildpath at the end of the pattern.
        """
        s_path=self._normalize_path(pattern)
        if s_path[-1]==wildpath:
            return self.get_matching_subtree(s_path[:-1],wildkey,wildpath,only_leaves=False)
        dfs_tree,matched=self._dfs_pattern(s_path,self._data,wildkey,wildpath,match_leaves=only_leaves,wrap_nodes=False)
        if not matched:
            return self._make_similar_dict({},copy=False)
        return self._make_similar_dict(dfs_tree,copy=False)

class DictionaryDiff(collections.namedtuple("DictionaryDiff",["same","changed_from","changed_to","removed","added"])): # making Sphinx autodoc generate correct docstring
    """
    Describes a difference between the two dictionaries.
    
    Attributes:
        same (:class:`Dictionary`): Contains the leafs which is the same.
        changed_from (:class:`Dictionary`): Contains the leafs from the first dictionary which have different values in the second dictionary.
        changed_to (:class:`Dictionary`): Contains the leafs from the second dictionary which have different values in the first dictionary.
        removed (:class:`Dictionary`): Contains the leafs from the first dictionary which are absent in the second dictionary.
        added (:class:`Dictionary`): Contains the leafs from the second dictionary which are absent in the first dictionary.
    """

class DictionaryIntersection(collections.namedtuple("DictionaryIntersection",["common","individual"])): # making Sphinx autodoc generate correct docstring
    """
    Describes the result of finding intersection of multiple dictionaries.
    
    Attributes:
        common (:class:`Dictionary`): Contains the intersection of all dictionaries.
        individual ([:class:`Dictionary`]): Contains list of difference from intersection for all dictionaries.
    """

### Conversion to and from a tuple ###
### Used in .strdump module (see that module for more info) ###
def _dump_dictionary(d, dumpf):
    v=d.as_dict("nested")
    v=dumpf(v)
    return v,d._case_normalization
def _load_dictionary(v, loadf):
    d,case_normalization=v
    return Dictionary(loadf(d),case_normalization=case_normalization,copy=False)
strdump.dumper.add_class(Dictionary,_dump_dictionary,_load_dictionary,"dict",recursive=True)




class DictionaryPointer(Dictionary):
    """
    Similar to :class:`Dictionary`, but can point at one of the branches instead of the full dictionary.
    
    Effect is mostly equivalent to prepending some path to all queries.
    
    Args:
        root (dict or Dictionary): Complete tree.
        pointer: Path to the pointer location.
        case_normalization (str): Case normalization rules; can be ``None`` (no normalization, names are case-sensitive), ``'lower'`` or ``'upper'``.
        copy (bool): If ``True``, make copy of the supplied data; otherwise, just make it the root.
        
    Warning:
        If ``copy==False``, the root data is already assumed to be normalized. If it isn't, the behavior might be incorrect.
    """
    def __init__(self, root=None, pointer=None, case_normalization=None, copy=True):
        Dictionary.__init__(self,root=root,case_normalization=case_normalization,copy=copy)
        self._root=self._data
        if len(pointer)==0:
            self._path=[]
        else:
            self.move_to(pointer)
        
    def __str__(self):
        iterleafs=self.iternodes(ordered=True,to_visit="leafs",include_path=True)
        path_length=len(self.get_path())
        content="\n".join("'{0}': {1}".format("/".join(k[path_length:]),str(v)) for k,v in iterleafs)
        return "{0}(location = '{1}'; {2})".format(type(self).__name__,"/".join(self.get_path()),content)
    __repr__=__str__
    
    def _replace_root(self, value, branch_option="normalize", keep_dict=True):
        if self._path:
            self._data=self._root
            self._data=self._get_branch(self._path[:-1])
            self._attach_node(self._data,self._path[-1],value,branch_option=branch_option)
            self._data=self._data[self._path[-1]]
        else:
            Dictionary._replace_root(self,value,branch_option=branch_option,keep_dict=keep_dict)
            self._root=self._data
    def get_path(self):
        """
        Return pointer path in the whole dictionary.
        """
        return self._path
    def move_to(self, path="", absolute=True):
        """
        Move the pointer to a new path.
        
        Args:
            path
            absolute (bool): If ``True``, path is specified with respect to the root;
                otherwise, it's specified with respect to the current position (and can only go deeper).
        """
        path=self._normalize_path(path)
        if not absolute:
            path=self._path+path
        self._path=path
        self._data=self._root
        self._data=self._get_branch(self._path)
        return self
    def move_up(self, levels, strict=True):
        """
        Move the pointer by the given number of levels up.
        
        If ``strict==True`` and there are not enough levels above, raise an error.
        Otherwise, stop at the top dictionary level.
        """
        if levels>0:
            if strict and len(self._path)<levels:
                raise KeyError("can not move the pointer {} levels up; only {} levels available".format(levels,len(self._path)))
            return self.move_to(self._path[:-levels])
        return self
        
    @staticmethod
    def _fast_build(root, norm_path, node, case_normalization=None, copy=False):
        ptr=DictionaryPointer(root=root,pointer=[],case_normalization=case_normalization,copy=copy)
        ptr._data=node
        ptr._path=norm_path
        return ptr
    
    def branch_pointer(self, branch=""):
        """
        Get a :class:`DictionaryPointer` of a given branch.
        """
        branch=self._path+self._normalize_path(branch)
        return DictionaryPointer(self._root,branch,case_normalization=self._case_normalization,copy=False)








def combine_dictionaries(dicts, func, select="all", pass_missing=False):
    """
    Combine several dictionaries element-wise (only for leafs) using a given function.

    Args:
        dicts(list or tuple): list of dictionaries (:class:`Dictionary` or ``dict``) to be combined
        func(callable): combination function. Takes a single argument, which is a list of elements to be combined.
        select(str): determines which keys are selected for the resulting dictionary.
            Can be either ``"all"`` (only keep keys which are present in all the dictionaries), or ``"any"`` (keep keys which are present in at least one dictionary).
            Only keys that point to leafs count; if a key points to a non-leaf branch in some dictionary, it is considered absent from this dictionary.
        pass_missing(bool): if ``select=="any"``, this parameter determines whether missing elements will be passed to `func` as ``None``, or omitted entirely.
    """
    funcargparse.check_parameter_range(select,"select",["all","any"])
    if not dicts:
        return Dictionary()
    dicts=[as_dictionary(d) for d in dicts]
    paths=set(dicts[0].paths())
    if select=="all":
        paths=set([p for p in paths if all([d.has_entry(p,kind="leaf") for d in dicts]) ])
    else:
        for d in dicts:
            paths.update(d.paths())
    result=dicts[0]._make_similar_dict()
    for p in paths:
        if select=="any" and pass_missing:
            values=[d[p] for d in dicts if d.has_entry(p,"leaf")]
        else:
            values=[(d[p] if d.has_entry(p,"leaf") else None) for d in dicts]
        joined_value=func(values)
        result[p]=joined_value
    return result
    
    








class PrefixTree(Dictionary):
    """
    Expansion of a :class:`Dictionary` designed to store data related to prefixes.
    
    Each branch node can have a leaf with a name given by wildcard (``'*'`` by default) or matchcard (``'.'`` by default).
    Wildcard assumes that the branch node path is a prefix; matchcard assumes exact match.
    These leafs are inspected when specific prefix tree functions (:meth:`find_largest_prefix` and :meth:`find_all_prefixes`) are used.
        
    Args:
        root (dict or Dictionary): Complete tree.
        case_normalization (str): Case normalization rules; can be ``None`` (no normalization, names are case-sensitive), ``'lower'`` or ``'upper'``.
        wildcard (str): Symbol for a wildcard entry.
        matchcard (str): Symbol for a matchcard entry.
        copy (bool): If ``True``, make copy of the supplied data; otherwise, just make it the root.
        
    Warning:
        If ``copy==False``, the root data is already assumed to be normalized. If it isn't, the behavior might be incorrect.
    """
    def __init__(self, root=None, case_normalization=None, wildcard="*", matchcard=".", copy=True):
        Dictionary.__init__(self,root,case_normalization=case_normalization,copy=copy)
        self._wildcard=wildcard
        self._matchcard=matchcard
    
    def copy(self):
        """Get a full copy the prefix tree"""
        return PrefixTree(self.branch_copy(),case_normalization=self._case_normalization,
                          wildcard=self._wildcard,matchcard=self._matchcard,copy=False)
        
    def _loop_over_prefixes(self, path, allow_nomatch_exact=True):
        s_path=self._normalize_path(path)
        l=len(s_path)
        branch=self._data
        for i,p in enumerate(s_path):
            if not self._is_branch(branch):
                return
            if self._wildcard in branch:
                yield i,branch[self._wildcard]
            if p in branch:
                branch=branch[p]
            else:
                return
        if not self._is_branch(branch):
            if allow_nomatch_exact:
                #yield None,branch
                yield l,branch
        else:
            if self._wildcard in branch:
                yield l,branch[self._wildcard]
            if self._matchcard in branch:
                yield l,branch[self._matchcard]
    def find_largest_prefix(self, path, default=None, allow_nomatch_exact=True, return_path=False, return_subpath=False):
        """
        Find the entry which is the largest prefix of a given path.
        
        Args:
            path
            default: Default value if the path isn't found.
            allow_nomatch_exact (bool): If ``True``, just element with the given path can be returned;
                otherwise, only elements stored under wildcards and matchcards are considered.
            return_path (bool): If ``True``, return path to the element (i.e., the largest prefix) instead of the element itself.
            return_subpath (bool): If ``True``, return tuple with a second element being part of the `path` left after subtraction of the prefix.
        """
        s_path=self._normalize_path(path)
        cut_pos=0
        data=default
        for l in self._loop_over_prefixes(s_path,allow_nomatch_exact=allow_nomatch_exact):
            cut_pos,data=l
        if return_subpath:
            return (s_path[:cut_pos] if return_path else data),s_path[cut_pos:]
        else:
            return (s_path[:cut_pos] if return_path else data)
    def find_all_prefixes(self, path, allow_nomatch_exact=True, return_path=True, return_subpath=False):
        """
        Find list of all the entries which are prefixes of a given path.
        
        Args:
            path
            default: Default value if the path isn't found.
            allow_nomatch_exact (bool): If ``True``, just element with the given path can be returned;
                otherwise, only elements stored under wildcards and matchcards are considered.
            return_path (bool): If ``True``, return path to the element (i.e., the largest prefix) instead of the element itself.
            return_subpath (bool): If ``True``, return tuple with a second element being part of the `path` left after subtraction of the prefix.
        """
        s_path=self._normalize_path(path)
        pfxs=[]
        for l in self._loop_over_prefixes(s_path,allow_nomatch_exact=allow_nomatch_exact):
            cut_pos,data=l
            if return_subpath:
                pfxs.append( ((s_path[:cut_pos] if return_path else data),s_path[cut_pos:]) )
            else:
                pfxs.append( (s_path[:cut_pos] if return_path else data) )
        return pfxs




class FilterTree(Dictionary):
    """
    Expansion of a :class:`Dictionary` designed to store hierarchical path filtering rules.

    Store path templates and the corresponding values (usually ``True`` or ``False`` for a filter tree, but other values are possible).
    The :meth:`match` method is then tested against this templates, and the value of the closest matching template (or default value, if none match) is returned.
    The templates can contain direct matches (e.g., ``"a/b/c"``, which matches only ``"a/b/c/"`` path),
    ``"*"`` path entries for a single level wildcard (e.g., ``"a/*/c"`` matches ``"a/b/c"`` or ``'a/d/c"``, but not ``"a/c"`` or ``"a/b/d/c"``),
    or ``"**"`` path entries for a multi-level wildcard (e.g., ``"a/**/c"`` matches ``"a/b/c"``, ``"a/c"``, or ``"a/b/d/c"``).
    The paths are always tested first for direct match, then for ``"*"`` match, then for ``"**"`` match starting from the smallest subpath matching ``"**"``.
    
    Args:
        root (dict or Dictionary): A filter tree or a list of filter tree paths (which are all assumed to be have the ``True`` value).s
        case_normalization (str): Case normalization rules; can be ``None`` (no normalization, names are case-sensitive), ``'lower'`` or ``'upper'``.
        default: Default value to return if no match is found.
        match_prefix: if ``True``, match the result even if only its prefix matches the tree content (same effect as adding ``"/**"`` to every tree path)
        copy (bool): If ``True``, make copy of the supplied data; otherwise, just make it the root.
        
    Warning:
        If ``copy==False``, the root data is already assumed to be normalized. If it isn't, the behavior might be incorrect.
    """
    def __init__(self, root=None, case_normalization=None, default=False, match_prefix=False, copy=True):
        if isinstance(root,list):
            root={p:True for p in root}
        Dictionary.__init__(self,root,case_normalization=case_normalization,copy=copy)
        self._default=default
        self._match_prefix=match_prefix
    
    def copy(self):
        """Get a full copy the prefix tree"""
        return FilterTree(self.branch_copy(),case_normalization=self._case_normalization,
            default=self._default,match_prefix=self._match_prefix,copy=False)
    
    def _match_subpath(self, branch, path):
        if not self._is_branch(branch):
            if len(path)==0 or self._match_prefix:
                return (branch,)
            else:
                return None
        if len(path)==0:
            return None
        name=path[0]
        if name in branch:
            return self._match_subpath(branch[name],path[1:])
        elif "*" in branch:
            return self._match_subpath(branch["*"],path[1:])
        elif "**" in branch:
            for p in range(len(path)):
                res=self._match_subpath(branch["**"],path[p:])
                if res is not None:
                    return res
        return None
    def match(self, path):
        """Return the match result for the path"""
        path=self._normalize_path(path)
        root=self._data
        result=self._match_subpath(root,path)
        if result is None:
            return self._default
        else:
            return result[0]





class PrefixShortcutTree:
    """
    Convenient storage for dictionary path shortcuts.
    
    Args:
        shortcuts (dict): Dictionary of shortcuts ``{shortcut: full_path}``.
    """
    def __init__(self, shortcuts=None):
        self._tree=PrefixTree()
        if shortcuts:
            self.add_shortcuts(shortcuts)
            
    def copy(self):
        """Return full copy"""
        res=PrefixShortcutTree()
        res._tree=self._tree.copy()
        return res
    def add_shortcut(self, source, dest, exact=False):
        """
        Add a single shortcut.
        
        Args:
            source: Shortcut path.
            dest: expanded path corresponding to the shortcut.
            exact (bool): If ``True``, the shortcut works only for the exact path; otherwise, it works for any path with 'source' as a prefix.
        """
        self._tree[source,"." if exact else "*"]=normalize_path(dest)
        return self
    def add_shortcuts(self, shortcuts, exact=False):
        """
        Add a dictionary of shortcuts ``{shortcut: full_path}``.
        
        Arguments are the same as in :meth:`PrefixShortcutTree.add_shortcut`.
        """
        for s,d in shortcuts.items():
            self.add_shortcut(s,d,exact=exact)
        return self
    def remove_shortcut(self, source):
        """Remove a shortcut from the tree"""
        pfx=self._tree.find_largest_prefix(source,return_path=True)
        del self._tree[pfx]
    def updated(self, shortcuts, exact=False):
        """
        Make a copy and add additional shortcuts.
        
        Arguments are the same as in :meth:`PrefixShortcutTree.add_shortcuts`.
        """
        return self.copy().add_shortcuts(shortcuts,exact=exact)

    def _find_shortcut(self, source):
        dest,subpath=self._tree.find_largest_prefix(source,return_subpath=True)
        if dest and subpath:
            dest=dest+subpath
        return dest
    def __call__(self, source, recursive=True):
        """
        Find and expand shortcuts in the path.
        
        Args:
            source: Source path.
            recursive (bool): If ``True``, keep substituting shortcuts while possible; otherwise, do a single substitute.
        """
        source=normalize_path(source)
        if recursive:
            while True:
                dest=self._find_shortcut(source)
                if dest is None:
                    return source
                source=dest
        else:
            return self._find_shortcut(source) or source


    




## Generate (local) objects hierarchy from Dictionary
## local here means that object is created based only on its immediate children, not on grand children or parents
class DictionaryNode:
    def __init__(self, **vargs):
        for name,value in vargs.items():
            setattr(self,name,value)
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "DictionaryNode({})".format(self)
def _default_object_generator(data, name=None):  # pylint: disable=unused-argument
    return DictionaryNode(**data)
def dict_to_object_local(data, name=None, object_generator=_default_object_generator):
    obj_dict={}
    for name,value in data.items():
        if Dictionary._is_branch(value):
            obj_dict[name]=dict_to_object_local(value,name=name,object_generator=object_generator)
        else:
            obj_dict[name]=value
    return object_generator(obj_dict,name)








### Indexing accessor decorator ###

class ItemAccessor:
    """
    Simple wrapper which implements array interface using supplied methods.

    Also has an option to normalize requested paths (enabled by default)

    Args:
        getter: method for getting values (``None`` means none is supplied, so getting raises an error)
        setter: method for setting values (``None`` means none is supplied, so setting raises an error)
        deleter: method for deleting values (``None`` means none is supplied, so deleting raises an error)
        contains_checker: method for checking if variable is present
            (``None`` means none is supplied, so checking containment raises an error; ``"auto"`` means that getter raising :exc:`KeyError` is used for checking)
        normalize_names: if ``True``, normalize a supplied path using the standard :class:`Dictionary` rules and join it into a single string using the supplied separator
        path_separator: path separator regex used for splitting and joining the supplied paths (by default, the standard ``"/"`` separator)
        missing_error: if not ``None``, specifies the error raised on the missing value;
            used in ``__contains__``, :meth:`get` and :meth:`setdefault` to determine if the value is missing
    """
    def __init__(self, getter=None, setter=None, deleter=None, iterator=None, contains_checker="auto", normalize_names=True, path_separator=None, missing_error=None):
        self.getter=getter
        self.setter=setter
        self.deleter=deleter
        self.iterator=iterator
        self.contains_checker=contains_checker
        self.normalize_names=normalize_names
        self.path_separator=path_separator
        self.missing_error=missing_error or KeyError
    def _norm_name(self, name):
        if self.normalize_names:
            return "/".join(normalize_path(name,sep=self.path_separator))
        return name
    def __iter__(self):
        if self.iterator is not None:
            return self.iterator().__iter__()
        raise TypeError("'{}' object is not iterable".format(type(self).__name__))
    def __getitem__(self, name):
        name=self._norm_name(name)
        if self.getter is not None:
            return self.getter(name)
        raise NotImplementedError("getter is not specified")
    def __setitem__(self, name, value):
        name=self._norm_name(name)
        if self.setter is not None:
            return self.setter(name, value)
        raise NotImplementedError("setter is not specified")
    def __delitem__(self, name):
        name=self._norm_name(name)
        if self.deleter is not None:
            return self.deleter(name)
        raise NotImplementedError("deleter is not specified")
    def __contains__(self, name):
        name=self._norm_name(name)
        if self.contains_checker=="auto" and self.getter is not None:
            try:
                self.getter(name)
                return True
            except self.missing_error:
                return False
        elif self.contains_checker is not None:
            return self.contains_checker(name)
        raise NotImplementedError("contains checker is not specified")
    def get(self, name, default=None):
        try:
            return self[name]
        except self.missing_error:
            return default
    def setdefault(self, name, default=None):
        try:
            return self[name]
        except self.missing_error:
            self[name]=default
            return self[name]