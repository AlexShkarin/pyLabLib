import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-q","--quiet",action="store_true",help="run in quiet (no output) mode")
parser.add_argument("--device-server",action="store_true",help="start the device server")
args=parser.parse_args()

if args.device_server:
    from .core.utils import net, rpyc_utils
    hostips=net.get_all_local_addr()
    hostnames=net.get_local_hostname(full=False),net.get_local_hostname(full=True)
    port=18812
    if not args.quiet:
        hostips_list=", ".join(["{}:{}".format(ip,port) for ip in hostips])
        print("Running device service at {} ({}), IP {}".format(hostnames[0],hostnames[1],hostips_list))
    rpyc_utils.run_device_service(verbose=not args.quiet,port=port)