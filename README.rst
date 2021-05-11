Overview
=======================

PyLabLib is a collection of code for external device control, data acquisition, and experiment automation.

Some major parts include:
    - A variety of `devices <http://pylablib.readthedocs.io/en/latest/devices/devices_root.html>`__, including several different `camera interfaces <http://pylablib.readthedocs.io/en/latest/devices/cameras_root.html>`__, `translational stages <http://pylablib.readthedocs.io/en/latest/devices/stages_root.html>`__, `oscilloscopes <http://pylablib.readthedocs.io/en/latest/devices/Tektronix.html>`__, `AWGs <http://pylablib.readthedocs.io/en/latest/devices/generic_awgs.html>`__, `sensors <http://pylablib.readthedocs.io/en/latest/devices/basic_sensors_root.html>`__, etc. The set is constantly expanding.
    - Simplified data processing utilities: convenient `fitting <http://pylablib.readthedocs.io/en/latest/dataproc.html#fitting>`__, `filtering <http://pylablib.readthedocs.io/en/latest/dataproc.html#filtering-and-decimation>`__, `feature detection <http://pylablib.readthedocs.io/en/latest/dataproc.html#feature-detection>`__, `FFT <http://pylablib.readthedocs.io/en/latest/dataproc.html#fourier-transform>`__ (mostly wrappers around NumPy and SciPy).
    - Universal multi-level `dictionaries <http://pylablib.readthedocs.io/en/latest/storage.html#multi-level-dictionary>`__ which are convenient for `storing <http://pylablib.readthedocs.io/en/latest/storage.html#dictionary-files>`__ heterogeneous data and settings in human-readable format.
    - Assorted functions for dealing with `file system <http://pylablib.readthedocs.io/en/latest/misc_utils.html#file-system>`__ (creating, moving and removing folders, zipping/unzipping, path normalization), `network <http://pylablib.readthedocs.io/en/latest/misc_utils.html#network>`__ (simplified interface for client and server sockets), `strings <http://pylablib.readthedocs.io/en/latest/misc_utils.html#strings>`__ (conversion of various Python objects to and from string), and more.
    - Tools for GUI generation and advanced multi-threading built on top of Qt5 *(still in development stage: the documentation is incomplete, and the interfaces can change in later versions)*

The most recent version of the library is available on GitHub (https://github.com/AlexShkarin/pyLabLib), and the documentation can be found at http://pylablib.readthedocs.io/ .