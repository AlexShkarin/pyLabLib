pip install -U wheel twine
del /Q build
del /Q dist
python setup.py sdist bdist_wheel
REM twine upload dist/*
twine upload --repository testpypi dist/*
REM pip install --extra-index-url https://testpypi.python.org/pypi pylablib[devio,gui]