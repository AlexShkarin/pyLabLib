import subprocess
import argparse
import shutil


def clear_build():
    shutil.rmtree(".apidoc",ignore_errors=True)
    shutil.rmtree("_build",ignore_errors=True)


def make(apidoc=True, builder="html"):
    if apidoc:
        subprocess.call(["python","apidoc_noautogen.py"])
    subprocess.call(["sphinx-build","-M",builder,".","_build"])


parser=argparse.ArgumentParser()
parser.add_argument("-c","--clear",action="store_true")
parser.add_argument("--noapidoc",action="store_true")
args=parser.parse_args()

if args.clear:
    print("Clearing build\n")
    clear_build()
make(apidoc=not args.noapidoc)