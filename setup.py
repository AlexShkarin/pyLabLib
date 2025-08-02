"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import Extension, setup, find_packages
from codecs import open
from os import path
import pathlib

here = path.abspath(path.dirname(__file__))

with open(path.join(here,'README.md')) as f:
    long_description=f.read()

def list_cython_extensions(folder="pylablib"):
    exts=[]
    for f in pathlib.Path(folder).glob(path.join("**","*.pyx")):
        name=".".join(list(f.parts[:-1])+[path.splitext(f.parts[-1])[0]])
        exts.append(Extension(name=name,sources=[str(f)],optional=True))
    return exts

dep_base=['numpy','scipy','pandas']
dep_extra=['rpyc','numba']
dep_devio=['pyft232','pyvisa>=1.6','pyserial','pyusb']
dep_devio_extra=['nidaqmx','websocket-client']
dep_pyqt5=['pyqt5>=5.9','pyqtgraph']
dep_pyside2=['pyside2','shiboken2','pyqtgraph>0.10']
setup(
    name='pylablib',
    # name='pylablib-lightweight',
    version='1.4.4',
    description='Code for use in lab environment: experiment automation, data acquisition, device communication',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AlexShkarin/pyLabLib',
    author='Alexey Shkarin',
    author_email='pylablib@gmail.com',
    license="GPLv3",
    classifiers=[
    'Development Status :: 4 - Beta',
    'Operating System :: Microsoft :: Windows',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    ],
    project_urls={
    'Documentation': 'https://pylablib.readthedocs.io',
    'Source': 'https://github.com/AlexShkarin/pyLabLib/',
    'Tracker': 'https://github.com/AlexShkarin/pyLabLib/issues'
    },
    packages=find_packages(include=['pylablib*']),
    ext_modules=list_cython_extensions(),
    install_requires=dep_base+dep_extra+dep_devio+dep_pyqt5,
    extras_require={
        'devio-full':dep_devio_extra,
    },
    # install_requires=dep_base,
    # extras_require={
    #     'extra':dep_extra,
    #     'devio':dep_devio,
    #     'devio-full':dep_devio+dep_devio_extra,
    #     'gui-pyqt5':dep_pyqt5,
    #     'gui-pyside2':dep_pyside2,
    # }
)