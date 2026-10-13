## Overview

[![10.5281/zenodo.7324875](https://zenodo.org/badge/DOI/10.5281/zenodo.7324875.svg)](https://doi.org/10.5281/zenodo.7324875)

PyLabLib aims to provide support for device control and experiment automation. It interfaces with lots of different [devices](https://pylablib.readthedocs.io/en/latest/devices/devices_root.html), including several different [camera interfaces](https://pylablib.readthedocs.io/en/latest/devices/cameras_root.html), [translational stages](https://pylablib.readthedocs.io/en/latest/devices/stages_root.html), [oscilloscopes](https://pylablib.readthedocs.io/en/latest/devices/Tektronix.html), [AWGs](https://pylablib.readthedocs.io/en/latest/devices/generic_awgs.html), [sensors](https://pylablib.readthedocs.io/en/latest/devices/basic_sensors_root.html), and more. The interface is implemented in a natural way through Python objects, and is easy to understand. For example, here is a complete script which steps Thorlabs KDC101 stage by 10000 steps ten times, and each time grabs a frame with Andor iXon camera:

```python

    from pylablib.devices import Thorlabs, Andor  # import the device libraries
    import numpy as np  # import numpy for saving

    # connect to the devices
    with Thorlabs.KinesisMotor("27000000") as stage, Andor.AndorSDK2Camera() as cam:
        # change some camera parameters
        cam.set_exposure(50E-3)
        cam.set_roi(0, 128, 0, 128, hbin=2, vbin=2)
        # start the stepping loop
        images = []
        for _ in range(10):
            stage.move_by(10000)  # initiate a move
            stage.wait_move()  # wait until it's done
            img = cam.snap()  # grab a single frame
            images.append(img)

    np.array(images).astype("<u2").tofile("frames.bin")  # save frames as raw binary
```

The list of the devices is constantly expanding.

Additional utilities are added to simplify data acquisition, storage, and processing:

- Simplified data processing utilities: convenient [fitting](https://pylablib.readthedocs.io/en/latest/dataproc.html#fitting), [filtering](https://pylablib.readthedocs.io/en/latest/dataproc.html#filtering-and-decimation), [feature detection](https://pylablib.readthedocs.io/en/latest/dataproc.html#feature-detection), [FFT](https://pylablib.readthedocs.io/en/latest/dataproc.html#fourier-transform) (mostly wrappers around NumPy and SciPy).
- Universal multi-level [dictionaries](https://pylablib.readthedocs.io/en/latest/storage.html#multi-level-dictionary) which are convenient for [storing](https://pylablib.readthedocs.io/en/latest/storage.html#dictionary-files) heterogeneous data and settings in human-readable format.
- Assorted functions for dealing with [file system](https://pylablib.readthedocs.io/en/latest/misc_utils.html#file-system) (creating, moving and removing folders, zipping/unzipping, path normalization), [network](https://pylablib.readthedocs.io/en/latest/misc_utils.html#network) (simplified interface for client and server sockets), [strings](https://pylablib.readthedocs.io/en/latest/misc_utils.html#strings) (conversion of various Python objects to and from string), and more.

The most recent version of the library is available on GitHub (https://github.com/AlexShkarin/pyLabLib), and the documentation can be found at https://pylablib.readthedocs.io/ .


## Requirements

- Python 3 (tested with 3.6+)
- Most extensively tested with Windows 10 and 64-bit Python. Linux is, in principle, supported, but devices which require manufacturer-provided DLLs (mostly cameras) might, potentially, have problems.
- Basic version only needs numpy, SciPy and pandas. Advanced device communication packages (such as [PyVISA](https://pyvisa.readthedocs.io/en/latest/) and [pySerial](https://pythonhosted.org/pyserial/)) are automatically installed, but can be avoided if necessary.
- Some devices might require [additional software](https://pylablib.readthedocs.io/en/latest/devices/devices_basics.html#dependencies-and-external-software). If this is the case, the requirements are mentioned on the corresponding page.


## Installation

### Install this fork from GitHub

Use the Python interpreter from the environment where you want the package installed. In an activated virtual environment, run:

```sh
python -m pip install "git+https://github.com/bhathawayy/pyLabLib.git"
```

To clone the fork and work on its source code instead:

```sh
git clone https://github.com/bhathawayy/pyLabLib.git
cd pyLabLib
python -m pip install -e .
```

Check the interpreter before installing if you have multiple Python environments:

```sh
python -c "import sys; print(sys.executable)"
```

If Git reports `SEC_E_UNTRUSTED_ROOT` while cloning on Windows, the computer does not trust the HTTPS certificate it received. This happens before the package build starts. Check the computer's date and time and its trusted root certificates; on a managed network, ask your IT team about the network's certificate authority. Keep Git's certificate verification enabled.

You can also test Git's OpenSSL certificate backend, which still verifies the server certificate:

```sh
git -c http.sslBackend=openssl ls-remote https://github.com/bhathawayy/pyLabLib.git HEAD
```

If that succeeds, set it for your Git user and retry the installation:

```sh
git config --global http.sslBackend openssl
```

The upstream release is available from [PyPI](https://pypi.org/project/pylablib/) as `pylablib`. Installing that name from PyPI does not install this fork. More upstream installation options are in the [documentation](https://pylablib.readthedocs.io/en/latest/install.html).


## Related projects

[Pylablib cam-control](https://github.com/AlexShkarin/pylablib-cam-control) - software for universal camera control and frames acquisition.
