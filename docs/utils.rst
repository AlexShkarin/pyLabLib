=========
Utilities
=========

----------------------
Multi-level dictionary
----------------------

:class:`.dictionary.Dictionary` is an expansion of the standard `dict` class which supports tree structures (nested dictionaries). The extensions include:

- handling multi-level paths and nested dictionaries, with several different indexing methods
- iteration over the immediate branches, or over the whole tree structure
- some additional methods: mapping, filtering, finding difference between two dictionaries
- combined with :mod:`pylablib.core.fileio` allows to save and load the content in a human-readable format.

Creating and indexing::

    >>> d = pll.Dictionary()
    >>> d['d/0/x'] = 5
    >>> d
    Dictionary('d/0/x': 5)
    >>> d['d/0/x']  # string path indexing
    5
    >>> d['d']['0']['x']  # nested indexing
    5
    >>> d['d','0','x']  # multi-level path indexing
    5
    >>> d['d',0,'x']  # all path elements are converted into strings
    5
    >>> d['d/0']['x']  # indexing styles can be freely mixed
    5
    >>> d['d','0/x']
    5
    >>> b = d['d']  # indexing a branch yields another Dictionary object
    >>> b
    Dictionary('0/x': 5)
    >>> b['0/x'] = 10  # the branch shares the data with the main dictionary
    >>> d
    Dictionary('d/0/x': 10)

A dictionary can be build from a Python ``dict``, which automatically normalizes paths and nested dictionaries::

    >>> d = pll.Dictionary({ 'a':1, 'b/i':2, 'c':{'i':3, 'ii':4}, 'd/0/x':5 })
    >>> d
    Dictionary('b/i': 2
    'c/i': 3
    'c/ii': 4
    'd/0/x': 5
    'a': 1)

.. note::
    There are several limitations on the dictionary structure (mostly they involve possible paths and keys):

        - As mentioned above, the keys are converted into strings to get the path; therefore, different Python object can merge together (e.g., number ``0`` and string literal ``'0'``). This also discourages use of some of the objects with "underdefined" (implementation dependent) representations, for example, floating point numbers.
        - Since the ``'/'`` symbol is used to split different path entries, it can't be used inside a single-level key. It is possible to re-define this symbol on dictionary creation; however, it might lead to compatibility issues.
        - Using spaces is in principle allowed; however, it leads to problems if the dictionary is saved to or loaded from a text file using standard methods, since there space is used to separate the path and the value (so a part of the path after the first space would become a part of the value). The same concerns other whitespace characters (``'\n'``, ``'\r'``, ``'\t'``).
        - Empty keys are not allowed. When building a path, they are automatically dropped, so ``'a/b'``, ``'a/b/'``, ``'a///b//'`` all correspond to the same path.
        - One path can either correspond to a branch node, or a leaf node. In other words, one path can't be a prefix of other paths and also contain data: structures like ``pll.Dictionary({ 'a':1, 'a/b':2})`` are not allowed. To get around this, one can define a specific "data key" not used anywhere else, and store data in a node under that key (e.g., with the data key ``'#'`` the example before turns into a valid structure ``pll.Dictionary({ 'a/#':1, 'a/b/#':2})``).

    Thus, it is generally recommended to only use strings or non-negative integers as keys, and apply the same restrictions to them as to the Python variable names (with the addition of names starting with a digit).