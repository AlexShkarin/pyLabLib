# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import re
import sphinx

from unittest import mock


# -- Project information -----------------------------------------------------

project = 'pylablib'
copyright = '2025, Alexey Shkarin'
author = 'Alexey Shkarin'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = '1.4.4'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
if os.path.exists(".apidoc") and len(os.listdir(".apidoc"))>0:
    extensions = ['sphinx.ext.autodoc']
else:
    extensions = []
extensions += [
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]
if sphinx.version_info[0]>=3:
    extensions+=['sphinxcontrib.spelling']

autodoc_mock_imports = ['nidaqmx', 'pyvisa', 'serial', 'ft232', 'PyQt5', 'pywinusb', 'pyqtgraph', 'websocket', 'matplotlib', 'sip', 'rpyc', 'numba', 'pandas']
sys.modules['pyvisa']=mock.Mock(VisaIOError=object, __version__='1.9.0')
sys.modules['serial']=mock.Mock(SerialException=object)
sys.modules['ft232']=mock.Mock(Ft232Exception=object)
sys.modules['PyQt5.QtCore']=mock.Mock(QObject=object,QThread=object)
sys.modules['PyQt5.QtWidgets']=mock.Mock(QWidget=object,QFrame=object,QGroupBox=object,QScrollArea=object,QTabWidget=object,
    QPushButton=object,QComboBox=object,QLineEdit=object,QLabel=object,QDialog=object)
sys.modules['PyQt5']=mock.Mock(QtCore=sys.modules['PyQt5.QtCore'],QtWidgets=sys.modules['PyQt5.QtWidgets'])
def nodec(*_, **__):
    return lambda f:f
sys.modules['numba']=mock.MagicMock(njit=nodec,jit=nodec)
if os.path.exists(".skipped_apidoc"):
    with open(".skipped_apidoc","r") as f:
        for ln in f.readlines():
            module=None
            m=re.match(r".*pylablib\\devices\\(.*_(?:lib|def))\.py$",ln.strip().replace("/","\\"))
            if m:
                module="pylablib.devices."+m[1].replace("\\",".")
            m=re.match(r".*pylablib\\(.*)\.(?:pyx|c)$",ln.strip().replace("/","\\"))
            if m:
                module="pylablib."+m[1].replace("\\",".")
            if module:
                sys.modules[module]=mock.Mock()
                print("Mocking {}".format(module))
autodoc_member_order='bysource'

nitpicky=False
nitpick_ignore=[("py:class","callable"),
                ("py:class","socket.socket"),
                ("py:class","builtins.OSError"), ("py:class","builtins.RuntimeError"),
                ("py:class","usb.core.USBError"), ("py:class","pyvisa.errors.VisaIOError"), ("py:class","rpyc.SlaveService"),
                ("py:class","sphinx.ext.autodoc.importer._MockObject"),
                ("py:class","builtins.object"),
                ]
intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'numpy': ('https://numpy.org/doc/stable/', None),
                       'pandas': ('https://pandas.pydata.org/pandas-docs/dev/', None),
                       'scipy': ('https://docs.scipy.org/doc/scipy/', None),
                       'matplotlib': ('https://matplotlib.org/stable/', None),
                       'rpyc': ('https://rpyc.readthedocs.io/en/latest/', None),
                       'pyqtgraph': ("https://pyqtgraph.readthedocs.io/en/latest/", None),
                       'pySerial': ("https://pythonhosted.org/pyserial/", None),
                       'PyVISA': ("https://pyvisa.readthedocs.io/en/latest/", None),
                       'nidaqmx': ("https://nidaqmx-python.readthedocs.io/en/latest/", None),}

spelling_word_list_filename=["../.pylintdict",".sphinxdict"]


duplicate_classes=set()
duplicate_classed_added=set()
namedtuple_att_ignore=set()
if os.path.exists(".autodoc_ignore"):
    with open(".autodoc_ignore","r") as f:
        for ln in f.readlines():
            ln=ln.strip()
            if ln and not ln.startswith("#"):
                k,n=ln.split(maxsplit=1)
                if k=="dup":
                    duplicate_classes.add(n)
                elif k=="ntatt":
                    namedtuple_att_ignore.add(n)
def remove_duplicates(app, what, name, obj, skip, options):
    if isinstance(obj,type):
        name="{}.{}".format(obj.__module__,obj.__name__)
        if name in duplicate_classes:
            if name in duplicate_classed_added:
                return True
            duplicate_classed_added.add(name)
    if name in ["count","index"] and str(obj)=="<method '{}' of 'tuple' objects>".format(name):
        return True
    if name in namedtuple_att_ignore and isinstance(obj,type) and issubclass(obj,tuple) and hasattr(obj,"_fields"):
        for f in obj._fields:
            try:
                delattr(obj,f)
            except AttributeError:
                pass
    return None
def no_namedtuple_attrib_docstring(app, what, name, obj, options, lines):
    if len(lines)==1 and lines[0].startswith('Alias for field number'):
        del lines[:]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False



# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

def setup(app):
    app.add_css_file('css/wide.css')
    app.connect('autodoc-process-docstring',no_namedtuple_attrib_docstring)
    app.connect('autodoc-skip-member',remove_duplicates)


# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'pylablibdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'pylablib.tex', 'pylablib Documentation',
     'Alexey Shkarin', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'pylablib', 'pylablib Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'pylablib', 'pylablib Documentation',
     author, 'pylablib', 'Code for use in lab environment: experiment automation, data acquisition, device communication.',
     'Miscellaneous'),
]



