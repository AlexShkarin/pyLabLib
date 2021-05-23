import numpy as np

def as_array(data, force_copy=False, try_object=True):
    """
    Turn `data` into a numpy array.

    If ``force_copy==True``, copy the data if it's already a numpy array.
    If ``try_object==False``, only try to convert to numerical numpy arrays; otherwise, generic numpy arrays (with ``dtype=="object"``) are acceptable.
    """
    try:
        return data.as_array(force_copy=force_copy)
    except AttributeError:
        if force_copy:
            try:
                return np.asarray(data)
            except ValueError:
                return np.asarray(data,dtype="object")
        else:
            try:
                return np.array(data)
            except ValueError:
                return np.array(data,dtype="object")
        
def get_shape(data, strict=False):
    """
    Get the data shape.

    If the data is a nested list and ``strict==True``, raise an error unless all sublists have the same length (i.e., the data is rectangular).
    """
    try:
        return data.shape
    except AttributeError:
        pass
    if np.isscalar(data):
        return ()
    if isinstance(data,list) or isinstance(data,tuple): # workaround, to reduce delay from NumPy converting list into array before getting its shape
        if len(data)>100: # for long lists, where looping can introduce lags
            return np.shape(data)
        shapes=[get_shape(x,strict=strict) for x in data]
        if len(shapes)==0:
            return (0,)
        elshape=shapes[0]
        for s in shapes[1:]:
            if s!=elshape:
                if strict:
                    raise ValueError("objects in the list have different shapes: {0}".format(shapes))
                else:
                    elshape=()
                    break
        return (len(shapes),)+elshape
    return ()