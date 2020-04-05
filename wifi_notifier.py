#!/usr/bin/env python

import subprocess
from subprocess import TimeoutExpired
import argparse
import platform
import time
from datetime import datetime

# set up the command line arguments                                             The formatter will show default values
parser = argparse.ArgumentParser(description="Notifier when wifi is back up.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                                                                          # choose better default targer
parser.add_argument("--host", metavar="hostname", type=str, nargs='?', default="google.com", help="The hostname to ping")
parser.add_argument("--count", metavar="N", type=str, nargs="?", default="2", help="The number of times the program should attemp to ping the host.")
parser.add_argument("--silent", action="store_true", help="Silent the output. Only show when network connection is back up.")
parser.add_argument("--seconds", type=int, choices=range(1, 10000), metavar="1-10000", nargs="?", default=3, help="How many seconds between the ping requests when there is no network connection (in seconds in the range  1-10000).")
parser.add_argument("--idle", type=int, choices=range(1, 10000), metavar="1-10000", nargs="?", default=600, help="How many seconds between the requests when you are connected to the internet.")
parser.add_argument("--save", type=argparse.FileType('w', encoding='UTF-8'), metavar="/path/to/file", nargs="?", help="Save the log to a file.")
parser.add_argument("--in", "-i", type=argparse.FileType('r'), metavar="/path/to/file", nargs="?", default="urls_to_download.txt", help="Path to the file containing the urls to download from (look at the urls_to_download.txt file for more information).")
# TODO check if it is a valid directory
parser.add_argument("--out", "-o", type=str, metavar="/path/to/folder", nargs="?", default="downloads/", help="Path to the folder where the url resources will be downloaded (look at the urls_to_download.txt file for more information).")
parser.add_argument("--visual", action="store_true", help="Show the log in a more visual way.")
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
    try:
        output = subprocess.run(["ping", parameter, args.count, "-w", "2",args.host], timeout=2, capture_output=True)
        if b"Temporary failure in name resolution" in output.stderr or output.returncode==2:
            raise TimeoutExpired("Cannot validate hostname", timeout=2)
    except(TimeoutExpired):
        while True:
            try:
                output = subprocess.run(["ping", parameter, args.count, "-w", "2",args.host], timeout=2, capture_output=True)
                # print(output)
                if b"Temporary failure in name resolution" in output.stderr or output.returncode==2:
                    raise TimeoutExpired("Cannot validate hostname", timeout=2)
                print("\r\n\r\nThere is network connection")
                break
            except(TimeoutExpired):
                count_expired+=10
            if not args.silent and count_expired % 10 == 0:
                print(datetime.now().strftime("%d %b [%H:%M:%S] "), "Trying to connect...")
            time.sleep(args.seconds)
    seconds = args.idle
    if seconds < 60:
        print("Trying again in", seconds, "second" if seconds == 1 else "seconds")
    elif seconds < 3600:
        print("Trying again in", seconds/60, "minute" if seconds == 60 else "minutes")
    elif seconds < 86400:
        print("Trying again in", seconds/3600, "hour" if seconds == 3600 else "hours")
    else:
        print("Trying again in", seconds/86400, "day" if seconds == 86400 else "days")

    time.sleep(args.idle)
    print("There is network connection")

# TODO persistence
# check for network connection every 10 minutes?
# TODO add formatted colored output (with clearing the screen and all)
# Also add parameters -i and -o for input file and output directory to download articles so that if the wifi goes down you could still read them.
# Add threads to download the articles when the program is run and to (try to ) keep downloading when the file is updated by the user
    # The file will be a list of urls separated by a /n.
    # When users add or remove urls from the file, the script will download/delete the articles from the urls (threaded file watcher)
# parse the file so that urls are separated by new lines and # and // are comments.
