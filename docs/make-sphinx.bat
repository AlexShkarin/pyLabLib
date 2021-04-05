del /Q .apidoc
sphinx-apidoc -o .apidoc ../pylablib "../pylablib/gui/**" "../pylablib/thread/**" "../pylablib/misc/**" "../pylablib/devices/**_defs.py" "../pylablib/devices/*/**_lib.py"
del /Q _build
make html