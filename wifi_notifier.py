#!/usr/bin/env python

import subprocess
import argparse
import platform

# set up the command line arguments
parser = argparse.ArgumentParser(description="Notifier when wifi is back up.")
                                                                          # choose better default targer
parser.add_argument("--host", metavar="hostname", type=str, nargs='?', default="google.com", help="The hostname to ping")
parser.add_argument("--count", metavar="N", type=str, nargs="?", default="2", help="The number of times the program should attemp to ping the host.")
args = parser.parse_args()

# ping -c 2 google.com     for linux
# ping -n 2 google.com     for windows

# depending on the os, ping requires different parameteres to specify count
if platform.system().lower() == "windows":
    parameter = "-n" 
else: 
    parameter = "-c"

print("Will start pinging", args.host, "until wifi is back up.")
subprocess.call(["ping", parameter, args.count, args.host])
