import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-q","--quiet",action="store_true",help="run in quiet (no output) mode")
parser.add_argument("--device-server",action="store_true",help="start the device server")
args=parser.parse_args()

if args.device_server:
    from .core.utils import rpyc_utils
    port=18812
    rpyc_utils.run_device_service(verbose=not args.quiet,port=port)