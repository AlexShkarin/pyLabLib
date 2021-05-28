"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here,'README.rst')) as f:
    long_description=f.read()

dep_base=['numpy','scipy','pandas']
dep_extra=['rpyc','numba']
dep_devio=['pyft232','pyvisa','pyserial','pyusb']
dep_devio_extra=['nidaqmx','websocket-client']
dep_pyqt5=['pyqt5','sip','pyqtgraph']
dep_pyside2=['pyside2','shiboken2','pyqtgraph']
setup(
    name='pylablib',
    # name='pylablib-lightweight',
    version='1.0.0',
    description='Collection of Python code for using in lab environment: experiment automation, data acquisition, device communication',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/AlexShkarin/pyLabLib',
    author='Alexey Shkarin',
    author_email='pylablib@gmail.com',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Operating System :: Microsoft :: Windows ',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Operating System :: Microsoft :: Windows'
    ],
    project_urls={
    'Documentation': 'https://pylablib.readthedocs.io',
    'Source': 'https://github.com/AlexShkarin/pyLabLib/',
    'Tracker': 'https://github.com/AlexShkarin/pyLabLib/issues'
    },
    packages=find_packages(include=['pylablib*'],exclude=['pylablib.thread*']),
    install_requires=dep_base+dep_extra+dep_devio+dep_devio_extra+dep_pyqt5,
    extras_require={
        'devio-full':['nidaqmx','websocket-client'],
    }
    # install_requires=dep_base,
    # extras_require={
    #     'extra':dep_extra,
    #     'devio':dep_devio,
    #     'devio-full':dep_devio+dep_devio_extra,
    #     'gui-pyqt5':dep_pyqt5,
    #     'gui-pyside2':dep_pyside2,
    # }
)