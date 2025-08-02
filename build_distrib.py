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
def make(wheel):
    subprocess.call(["python","setup.py","sdist"]+(["bdist_wheel"] if wheel else []))
def check():
    subprocess.call(["python","-m","twine","check","dist/*"])
def upload(production=False):
    if production:
        subprocess.call(["python","-m","twine","upload","--skip-existing","--verbose","dist/*"])
    else:
        subprocess.call(["python","-m","twine","upload","--repository","testpypi","--skip-existing","dist/*"])
        # pip install -U --no-cache-dir --extra-index-url https://testpypi.python.org/pypi pylablib


parser=argparse.ArgumentParser()
parser.add_argument("--update",action="store_true",help="Update wheel and twine packages before run")
parser.add_argument("-b","--build",action="store_true",help="clear the build and run setup.py")
parser.add_argument("-c","--check",action="store_true",help="check the build without rebuilding it")
parser.add_argument("-w","--wheel",action="store_true",help="build a wheel in addition to a pure Python distribution")
parser.add_argument("-u","--upload",action="store_true",help="upload to the server (testpy, unless -p is also specified)")
parser.add_argument("-p","--production",action="store_true",help="upload to the main pypi server (if -u is also specified)")
args=parser.parse_args()

if args.update:
    update()
if args.build:
    clear_build()
    make(args.wheel)
    check()
if args.check and not args.build:
    check()
if args.upload:
    upload(production=args.production)