import argparse
import os

parser=argparse.ArgumentParser()
parser.add_argument("-q","--quiet",action="store_true",help="run in quiet (no output) mode")
parser.add_argument("--device-server",action="store_true",help="start the device server")
parser.add_argument("--port",type=int,help="device server port",default=18812)
parser.add_argument("--config",help="path to a config file specifying library parameters")
args=parser.parse_args()

if args.config and os.path.exists(args.config):
    from . import load_par
    load_par(args.config)

if args.device_server:
    from .core.utils import rpyc_utils
    rpyc_utils.run_device_service(verbose=not args.quiet,port=args.port)