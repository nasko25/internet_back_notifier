#!/usr/bin/env python

import subprocess
from subprocess import TimeoutExpired
import argparse
import platform
import time

# set up the command line arguments
parser = argparse.ArgumentParser(description="Notifier when wifi is back up.")
                                                                          # choose better default targer
parser.add_argument("--host", metavar="hostname", type=str, nargs='?', default="google.com", help="The hostname to ping")
parser.add_argument("--count", metavar="N", type=str, nargs="?", default="2", help="The number of times the program should attemp to ping the host.")
parser.add_argument("--silent", action="store_true", help="Silent the output. Only show when network connection is back up.")
parser.add_argument("--seconds", type=int, choices=range(1, 10000), nargs="?", default=3, help="How many seconds between the ping requests when there is no network connection (in seconds in the range  1-10000).")
args = parser.parse_args()

# ping -c 2 google.com     for linux
# ping -n 2 google.com     for windows

# depending on the os, ping requires different parameteres to specify count
if platform.system().lower() == "windows":
    parameter = "-n" 
else: 
    parameter = "-c"

print("Will start pinging", args.host, "until wifi is back up.")

count_expired = 0
while True:
    time.sleep(args.seconds)
    try:
        output = subprocess.run(["ping", parameter, args.count, "-w", "2",args.host], timeout=2, capture_output=True)
        print(output)
        if b"Temporary failure in name resolution" in output.stderr or output.returncode==2:
            raise TimeoutExpired("Cannot validate hostname", timeout=2)
        break
    except(TimeoutExpired):
        count_expired+=10
    if not args.silent and count_expired % 10 == 0:
        print("Trying to connect...")

print("There is network connection")

# TODO persistence
# check for network connection every 10 minutes?
