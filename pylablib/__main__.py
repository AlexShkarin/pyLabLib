import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-q","--quiet",action="store_true",help="run in quiet (no output) mode")
parser.add_argument("--device-server",action="store_true",help="start the device server")
args=parser.parse_args()

if args.device_server:
    from .core.utils import net, rpyc_utils
    hostnames=net.get_all_local_addr()
    port=18812
    if not args.quiet:
        hostnames_list=", ".join(["{}:{}".format(hn,port) for hn in hostnames])
        print("Running device service at {}".format(hostnames_list))
    rpyc_utils.run_device_service(verbose=not args.quiet,port=port)