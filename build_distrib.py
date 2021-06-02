import subprocess
import argparse
import shutil


def update():
    subprocess.call(["python","-m","pip","install","-U","wheel","twine"])
def clear_build():
    shutil.rmtree("build",ignore_errors=True)
    shutil.rmtree("dist",ignore_errors=True)
    shutil.rmtree("pylablib.egg-info",ignore_errors=True)
    shutil.rmtree("pylablib_lightweight.egg-info",ignore_errors=True)
def make():
    subprocess.call(["python","setup.py","sdist","bdist_wheel"])
def upload(production=False):
    if production:
        subprocess.call(["python","-m","twine","upload","dist/*"])
    else:
        subprocess.call(["python","-m","twine","upload","--repository","testpypi","dist/*"])
        # pip install --extra-index-url https://testpypi.python.org/pypi pylablib


parser=argparse.ArgumentParser()
parser.add_argument("--update",action="store_true")
parser.add_argument("-u","--upload",action="store_true")
parser.add_argument("-p","--production",action="store_true")
args=parser.parse_args()

if args.update:
    update()
clear_build()
make()
if args.upload:
    upload(production=args.production)