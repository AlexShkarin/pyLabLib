import subprocess
import argparse
import shutil


def clear_build():
    shutil.rmtree(".apidoc",ignore_errors=True)
    shutil.rmtree("_build",ignore_errors=True)


def make(apidoc=True, builder="html", log=False, spell=False):
    if spell:
        comm=["sphinx-build","-b","spelling",".","_build"]
    else:
        if apidoc:
            subprocess.call(["python","apidoc_noautogen.py"])
        comm=["sphinx-build","-M",builder,".","_build"]
    if log:
        with open(".buildlogout","w") as fo, open(".buildlogerr","w") as fe:
            subprocess.call(comm,stdout=fo,stderr=fe)
    else:
        subprocess.call(comm)


parser=argparse.ArgumentParser()
parser.add_argument("-c","--clear",action="store_true")
parser.add_argument("-l","--log",action="store_true")
parser.add_argument("-s","--spell",action="store_true")
parser.add_argument("--noapidoc",action="store_true")
args=parser.parse_args()

if args.clear and not args.spell:
    print("Clearing build\n")
    clear_build()
make(apidoc=not args.noapidoc,log=args.log,spell=args.spell)