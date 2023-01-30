.. _misc_utils:

Various utilities
=========================

.. _misc_utils_files:

File system
-------------------------

There is a number of methods which are minor expansions of the built-in file utilities:

    - Accessing and changing file times: :func:`.utils.files.get_file_creation_time`, :func:`.utils.files.get_file_modification_time`, :func:`.utils.files.touch` (update the modification date).
    - Generating new file names (e.g., for storing a new dataset): :func:`.utils.files.generate_indexed_filename` and :func:`.utils.files.generate_prefixed_filename`.
    - Some path analysis methods: :func:`.utils.files.fullsplit`, :func:`.utils.files.normalize_path`, :func:`.utils.files.paths_equal`, :func:`.utils.files.relative_path`; a lot of these have also been implemented in :mod:`pathlib` module, and are kept for backwards compatibility.
    - Checking if a string is a valid path: :func:`.utils.files.is_path_valid`.
    - File copying and moving, which also creates containing folders if necessary: :func:`.utils.files.copy_file`, :func:`.utils.files.move_file`.
    - Folder creation and cleaning: :func:`.utils.files.ensure_dir`, :func:`.utils.files.remove_dir`, :func:`.utils.files.remove_dir_if_empty`, :func:`.utils.files.clean_dir`.
    - Analyzing folder content: :func:`.utils.files.list_dir`, :func:`.utils.files.list_dir_recursive`, :func:`.utils.files.dir_empty`, :func:`.utils.files.walk_dir`. Compared to the built-in methods, allows for more complicated (e.g., regex) filters for listed files and folders, as well as for visited folders.
    - Copying, moving, and comparing folders: :func:`.utils.files.copy_dir`, :func:`.utils.files.move_dir`, :func:`.utils.files.cmp_dirs`; like methods above, allows for regex filters for files and folders.
    - Retrying versions of most of the above methods: e.g., :func:`.utils.files.retry_move` or :func:`.utils.files.retry_clean_dir`. These functions try to copy/move/remove files or folders several times if errors arise, in case the files or folders are only temporarily blocked. Useful when, e.g., using network shares or some software which makes files or folders unavailable for a short period of time.
    - Wrapping methods for working with zip files: :func:`.utils.files.zip_folder`, :func:`.utils.files.zip_file`, :func:`.utils.files.zip_multiple_files`, :func:`.utils.files.unzip_folder`, :func:`.utils.files.unzip_file`.


.. _misc_utils_net:

Network
-------------------------

There is a simple wrapper class :class:`.utils.net.ClientSocket`, which simplifies some operations with the built-in :mod:`socket` module. In addition, it also implements a couple of higher-level ways to send the data: either fixed length (as in the usual socket), with the length prepended (in case the total length is initially unknown at the receiving end), or using a delimiter to mark the end of the message.

In addition, there are several methods for gaining local or remote host information (:func:`.utils.net.get_local_addr`, :func:`.utils.net.get_all_local_addr`, :func:`.utils.net.get_local_hostname`, :func:`.utils.net.get_all_remote_addr`, :func:`.utils.net.get_remote_hostname`), receiving JSON-formatted values (:func:`.utils.net.recv_JSON`), and listening on a given port (:func:`.utils.net.listen`).


.. _misc_utils_string:

Strings
-------------------------

There are several string manipulation functions present:

    - Powerful to/from string conversion. The main function are :func:`.utils.string.to_string` and :func:`.utils.string.from_string`, which can convert a large variety of values: simple scalar values (numbers, strings, booleans, ``None``), containers (lists, tuples, sets, dictionaries), escaped and byte strings (e.g., ``b"\x00"``), complex types such as numpy arrays (represented as, e.g., ``"array([0, 1, 2, 3, 4])"``). The latter version requires setting ``use_classes=True`` in :func:`.utils.string.to_string`, which is not enabled by default to make the results more compatible with other parsers::

        >> pll.to_string(np.arange(5))  # by default, use the standard str method, which makes array look like a list
        '[0, 1, 2, 3, 4]'
        >> pll.from_string('[0, 1, 2, 3, 4]')  # gets converted back into a list
        [0, 1, 2, 3, 4]
        >> pll.to_string(np.arange(5), use_classes=True)  # use representation class
        'array([0, 1, 2, 3, 4])'
        >> pll.from_string('array([0, 1, 2, 3, 4])')  # get converted back into an array
        array([0, 1, 2, 3, 4])

      More complex data classes can be added using :func:`.utils.string.add_conversion_class` and :func:`.utils.string.add_namedtuple_class`::

        >> NamedTuple = collections.namedtuple("NamedTuple", ["field1", "field2"])
        >> nt = NamedTuple(1,2)
        >> nt
        NamedTuple(field1=1, field2=2)
        >> pll.to_string(nt, use_classes=True)  # class is not registered, so use the default tuple representation
        '(1, 2)'
        >> pll.add_namedtuple_class(NamedTuple)
        >> pll.to_string(nt, use_classes=True)  # now the name marker is added
        'NamedTuple(1, 2)'
        >> pll.from_string('NamedTuple(1, 2)')
        NamedTuple(field1=1, field2=2)
        >> DifferentNamedTuple = collections.namedtuple("DifferentNamedTuple", ["field1", "field2"])
        >> pll.from_string('DifferentNamedTuple(1, 2)')  # note that if the class is not registered, it can't be parsed, so the string is returned back
        'DifferentNamedTuple(1, 2)'
    
      Furthermore, there is a couple of auxiliary string functions to parse more complicated situations: :func:`.utils.string.escape_string` and :func:`.utils.string.unescape_string` for escaping and unescaping string with potentially confusing or unprintable characters (e.g., quotation marks, spaces, new lines); :func:`.utils.string.from_string_partial`, :func:`.utils.string.from_row_string`, :func:`.utils.string.extract_escaped_string` to determine and extract the first value in a string which potentially has several values.
    
    - Comparing and searching string: :func:`.utils.string.string_equal` (compare string using different rules such as case sensitivity), :func:`.utils.string.find_list_string`, :func:`.utils.string.find_dict_string` (find string in a list or a dictionary using different comparison rules).
    - Filtering strings: :func:`.utils.string.get_string_filter`, :func:`.utils.string.sfglob`, and :func:`.utils.string.sfregex`. Creates filter functions which may include or exclude certain string patterns; these filter functions can be later used in, e.g., file-related methods such as :func:`.utils.files.list_dir`.


.. _misc_utils_misc:

Misc utilities
-------------------------

A variety of small useful methods and classes:

    - Dictionary manipulation functions: :func:`.utils.general.any_item` (get a random dict key-value pair), :func:`.utils.general.merge_dicts` (merge several dictionaries together), :func:`.utils.general.filter_dict` (filter dictionary according to key or value), :func:`.utils.general.map_dict_keys`, :func:`.utils.general.map_dict_values`, :func:`.utils.general.to_dict` (convert a dict or a list of pairs into a dictionary, using a default value for a non-pair list elements), :func:`.utils.general.invert_dict` (turn keys into values and vice versa).
    - List manipulation functions: :func:`.utils.general.flatten_list` (flatten a nested list structure), :func:`.utils.general.partition_list` (split a list into two lists according to a predicate), :func:`.utils.general.split_in_groups` (split list into several groups according to a key function), :func:`.utils.general.sort_set_by_list` (convert set into a list, whose values are sorted according to a second supplied list), :func:`.utils.general.compare_lists` (compare two lists and return their intersection and differences).
    - :class:`.utils.general.DummyResource`: a "dummy" resource class, which can be used in a ``with`` block but does nothing; can be used to, e.g., replace multi-threading resources such as locks to turn them off.
    - Unique ID generators: :class:`.utils.general.UIDGenerator` and :class:`.utils.general.NamedUIDGenerator`, which generate unique names (based on a counter), with a thread-safe option (useful to create, e.g., unique data markers).
    - Timekeeping: :class:`.utils.general.Countdown` for single shot and :class:`.utils.general.Timer` for repeating tasks. Simplifies dealing with operation timeouts: checking how much time is left (including options for infinite timeout), checking if timeout is passed, resetting, etc.
    - Script restarting via :func:`.utils.general.restart` (thread-controller style applications can also use :func:`.thread.controller.restart_app` for a more managed restart).
    - :class:`.utils.general.StreamFileLogger`, which can be set up to log all outputs into a stream (e.g., ``stdout``)::

        from pylablib import StreamFileLogger
        import sys
        sys.stderr = StreamLogger("logerr.txt", sys.stderr)  # replace stderr stream with a logged version
        # perform some tasks ...
        sys.stderr = sys.stderr.stream  # revert back, if necessary
    
      With the code above, all output to ``stderr`` will be logged into ``logerr.txt`` to be analyzed later. It can also be set with ``autoflush=True`` to automatically flush the printed text, which helps with identifying crushing bugs, and it can be supplied with a lock to help separate printouts from different threads.