.. _storage:

Data storage
=========================

Complex data storage in pylablib centers around 2 main components: the multi-level dictionary for representing hierarchical data within the code, and file IO to (among other things) load and store it in a human-readable format.

.. _storage_dictionary:

Multi-level dictionary
-------------------------

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
        - Empty keys are not allowed. When building a path, they are automatically dropped, so ``'a/b'``, ``'a/b/'``, ``'a///b//'`` all correspond to the same path.
        - One path can either correspond to a branch node, or a leaf node. In other words, one path can't be a prefix of other paths and also contain data: structures like ``pll.Dictionary({ 'a':1, 'a/b':2})`` are not allowed. To get around this, one can define a specific "data key" not used anywhere else, and store data in a node under that key (e.g., with the data key ``'#'`` the example before turns into a valid structure ``pll.Dictionary({ 'a/#':1, 'a/b/#':2})``).

    Thus, it is generally recommended to only use strings or non-negative integers as keys, and apply the same restrictions to them as to the Python variable names (with the addition of names starting with a digit).


.. _storage_fileio:

File IO
-------------------------

:mod:`pylablib.core.fileio` contains several function for saving and loading data into different kinds of files: binary (:func:`.loadfile.load_bin` and :func:`.savefile.save_bin`), CSV (:func:`.loadfile.load_csv` and :func:`.savefile.save_csv`), or dictionary (:func:`.loadfile.load_dict` and :func:`.savefile.save_dict`).

Binary files
~~~~~~~~~~~~~~~~~~~~~~~~~

The first (binary files) closely corresponds to numpy ``fromfile``. In addition, it also allows automatic conversion into pandas arrays, setting column names, and skipping some number of bytes from the start::

    >> table = np.arange(6).reshape((3,2))
    >> pll.save_bin(table, "table.dat", dtype="<f8)
    >> pll.load_bin("table.dat", columns=["Column1", "Column2"], dtype="<f8)
       Column1  Column2
    0      0.0      1.0
    1      2.0      3.0
    2      4.0      5.0

Furthermore, there is an option to save the binary data with a preamble dictionary file, which describes its structure (columns, dtype, etc.) This way, one does not have specify these parameter in the loading code::

    >> table = pd.DataFrame({"C1":arange(3),"C2":arange(3)**2/3})
    >> table
       C1        C2
    0   0  0.000000
    1   1  0.333333
    2   2  1.333333
    >> pll.save_bin_desc(table, "table.dat")
    >> pll.load_bin_desc("table.dat")
        C1        C2
    0  0.0  0.000000
    1  1.0  0.333333
    2  2.0  1.333333
    >> np.fromfile("table_data.bin", "<f8").reshape((3, 2))  # the data is still stored in the regular binary format
    array([[0.        , 0.        ],
           [1.        , 0.33333333],
           [2.        , 1.33333333]])

Note that only homogeneous data (i.e., all columns having the same type) is currently supported. That's why the first column got converted from integers into reals.

CSV files
~~~~~~~~~~~~~~~~~~~~~~~~~

The functionality of the second one mimics pandas ``read_csv``, but offers a bit more flexibility with more complicated values in columns, such as tuples or binary strings::

    >> table = pd.DataFrame({ "C1":np.arange(3), "C2":[(i**2,i**3) for i in range(3)] })
    >> table  # the second columns contains tuples
       C1      C2
    0   0  (0, 0)
    1   1  (1, 1)
    2   2  (4, 8)
    >> pll.save_csv(table, "table.csv")
    >> pll.load_csv("table.csv", dtype="generic")  # need to specify generic values type, which handle complicated cases, but is somewhat slower
       C1      C2
    0   0  (0, 0)
    1   1  (1, 1)
    2   2  (4, 8)


In addition, its default settings are a bit different: the column separator is a whitespace, the column names are contained in the comment string (which removes occasional ambiguity), and the creation date string is appended by default. Hence, the content of the file created above is

.. code-block:: none

    # C1	C2
    0	(0, 0)
    1	(1, 1)
    2	(4, 8)

    # Saved on 2021/01/01 12:00:00

Note that currently it operates only with simple flat tables and does not support advanced pandas features such as index or multi-index. If these are required, you can use :func:`.savefile.save_csv_desc` and :func:`.loadfile.load_csv_desc`. Similarly to :func:`.savefile.save_bin_desc` and :func:`.loadfile.load_bin_desc`, it saves a dictionary containing additional description; however, the table is inlined by default, so only one file is generated::

    >> table = pd.DataFrame({ "C1":np.arange(3), "C2":[(i**2,i**3) for i in range(3)] }, index=np.arange(3)+10)
    >> table  # non-trivial index colum
        C1      C2
    10   0  (0, 0)
    11   1  (1, 1)
    12   2  (4, 8)
    >> pll.save_csv(table, "table.csv")
    >> pll.load_csv("table.csv", dtype="generic")  # index is lost
        C1      C2
    0    0  (0, 0)
    1    1  (1, 1)
    2    2  (4, 8)
    >> pll.save_csv_desc(table, "table.dat")
    >> pll.load_csv_desc("table.dat")  # index is preserved (also note that here dtype is "generic" by default)
        C1      C2
    10   0  (0, 0)
    11   1  (1, 1)
    12   2  (4, 8)

.. _storage_fileio_dict:

Dictionary files
~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, dictionary saving and loading operates with :ref:`dictionary <storage_dictionary>` objects. It is generally useful to load or save various heterogeneous settings or parameters, such as device parameters, data processing parameters, and GUI or device state. It supports most basic Python data types as values: standard scalar types (integers, reals, complex numbers, strings, booleans, ``None``), containers (tuples, lists, dictionaries, sets, including nested ones), binary and raw string representation (e.g., ``b"\x00"`` or ``r"m\n\o"``), short numpy arrays (represented as, e.g., ``"array([1, 2, 3])"``), and inline tables (which are interpreted as pandas table by default). The only common data type not included is named tuples; they get automatically converted to regular tuples on saving.

The dictionary files have the ``key value`` line formats and typically use full paths (as opposed to, say, XML hierarchy), which makes them easier to inspect and parse without pylablib. For example, the dictionary from the previous section will be saved as

.. code-block:: none

    b/i 2
    c/i 3
    c/ii 4
    d/0/x 5
    a 1

With more complicated data types, it might look more like

.. code-block:: none

    process/points  array([1., 2., 3.])
    process/default/frequency   10+2.j
    # Lines starting with # are treated as comments
    plot/position   [(0,0), (1,1), (2,3)]
    plot/label  r"$\nu_0$"
    # Keys do not have to be in any particular order
    process/default/amplitude   5.

which results in a dictionary

.. code-block:: none

    Dictionary('plot/label': $\nu_0$
    'plot/position': [(0, 0), (1, 1), (2, 3)]
    'process/default/amplitude': 5.0
    'process/default/frequency': (10+2j)
    'process/points': [1. 2. 3.])

The format also supports hierarchy using ``//branch`` to mark a start of sub-branch and ``///`` to mark its end. For example, the dictionary above can be also saved as

.. code-block:: none

    //process
        # indentation is not required, but helps to see the structure
        points  array([1., 2., 3.])
        default/frequency   10+2.j
        default/amplitude   5.
    ///

    //plot
        position   [(0,0), (1,1), (2,3)]
        label  r"$\nu_0$"
    ///

Finally, it is possible to specify inline tables using special comment lines. For example,

.. code-block:: none

    # The key without the value marks the path to the table within the dictionary
    data/table
    ## Begin table
    1   1.j
    2   4.j
    3   9.j
    ## End table

produces a dictionary containing pandas DataFrame:

.. code-block:: none

    Dictionary('data/table':
       0                   1
    0  1  0.000000+1.000000j
    1  2  0.000000+4.000000j
    2  3  0.000000+9.000000j )