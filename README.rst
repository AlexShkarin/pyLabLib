Overview
=======================

PyLabLib is a collection of code intended to simplify some of the coding tasks encountered in a physics laboratory.

Some major parts include:
    - Simpler loading and saving of data in text or binary files.
    - Data tables with heterogeneous columns and more universal indexing (heavy overlap with pandas).
    - Some data processing utilities: filtering, decimating, peak detection, FFT (mostly wrappers around NumPy and SciPy).
    - Classes for device control (universal wrapper for pyVISA, pySerial and network backends).
    - Classes for many specific devices (cameras, lasers, translation stages, etc).
    - More user-friendly fitting interface.
    - Multi-level dictionaries which are convenient for storing heterogeneous data and settings in human-readable format.
    - A bunch more utilities dealing with file system (creating, moving and removing folders, zipping/unzipping, path normalization), network (simplified interface for client and server sockets), strings (serializing and de-serializing values), function introspection, and more.
    - Additional tools for GUI generation and simpler multithreading built on top PyQt5 *(still in development stage: not completely documented, code organization and interfaces can change in later versions)*.

The most recent version of the library is available on GitHub (https://github.com/AlexShkarin/pyLabLib), and the documentation can be found at http://pylablib.readthedocs.io/ .