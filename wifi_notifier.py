#!/usr/bin/env python

import subprocess
from subprocess import TimeoutExpired
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError
from urllib.error import URLError
import argparse
import platform
import time
import sys
import os
import threading
from datetime import datetime

try:
    if platform.system().lower() == "windows":
        import colorama
        # initilize colorama, so that the ansi color codes will work on windows as well
        colorama.init()
except ImportError:
    if platform.system().lower() == "windows":
        print("[WARNING] You don't have colorama, so the colored output will not work on windows.")

# set up the command line arguments                                             The formatter will show default values
parser = argparse.ArgumentParser(description="Notifier when wifi is back up.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                                                                          # choose better default target
parser.add_argument("--host", metavar="hostname", type=str, nargs='?', default="google.com", help="The hostname to ping")
parser.add_argument("--count", metavar="N", type=str, nargs="?", default="2", help="The number of times the program should attemp to ping the host.")
parser.add_argument("--silent", action="store_true", help="Silent the output. Only show when network connection is back up.")
parser.add_argument("--seconds", type=int, choices=range(1, 10000), metavar="1-10000", nargs="?", default=3, help="How many seconds between the ping requests when there is no network connection (in seconds in the range  1-10000).")
parser.add_argument("--idle", type=int, choices=range(0, 10000), metavar="0-10000", nargs="?", default=600, help="How many seconds between the requests when you are connected to the internet. Type in 0 if you want to quit after the internet is up.")
parser.add_argument("--save", type=argparse.FileType('a', encoding='UTF-8'), metavar="/path/to/file", nargs="?", help="Save the log to a file.")
parser.add_argument("--input", "--in", "-i", type=str, metavar="/path/to/file", nargs="?", default="urls_to_download.txt", help="Path to the file containing the urls to download from (look at the urls_to_download.txt file for more information).")
parser.add_argument("--out", "-o", type=str, metavar="/path/to/folder", nargs="?", default="downloads/", help="Path to the folder where the url resources will be downloaded (look at the urls_to_download.txt file for more information).")
parser.add_argument("--nodownload", action="store_true", help="Use this flag, if you do not want to download anything when you modify the urls_to_download.txt file.")
args = parser.parse_args()

# ping -c 2 google.com     for linux
# ping -n 2 google.com     for windows

# depending on the os, ping requires different parameteres to specify count
if platform.system().lower() == "windows":
    parameter = "-n"
else:
    parameter = "-c"

# Flag indicating whether the user has modified the file with the urls to download since the internet went down
modified_since_no_internet = False
# gobal list that will contain file paths of all urls currently in the urls_to_download.txt file
list_of_urls = []

# TODO refactor the platform.system().lower() == "windows" to a boolean variable ?
# TODO probably refactor if you at some point need more colors (can use the colorama color codes?)
def save(msg, **kwargs):
    if args.save != None:
        args.save.write(msg + "\n")

    if kwargs.get("color") != None:
                                    # end colored msg
        print(kwargs.get("color") + msg, "\033[0m")
    else:
        print(msg)

def main():
    save("Will start pinging " + args.host + " until wifi is back up.")

    count_expired = 0
    while True:
        try:
            output = subprocess.run(["ping", parameter, args.count, "-w", "2",args.host], timeout=2, capture_output=True)
                                                                       # windows return code is 1 for some reason
            if ((b"Temporary failure in name resolution" in output.stderr or output.returncode==2)
                    or (platform.system().lower() == "windows" and output.returncode==1)):
                raise TimeoutExpired("Cannot validate hostname", timeout=2)
        except(TimeoutExpired):
            while True:
                try:
                    output = subprocess.run(["ping", parameter, args.count, "-w", "2",args.host], timeout=2, capture_output=True)
                    # print(output)
                    if ((b"Temporary failure in name resolution" in output.stderr or output.returncode==2)
                            or (platform.system().lower() == "windows" and output.returncode==1)):
                        raise TimeoutExpired("Cannot validate hostname", timeout=2)
                    save("\r\n\r\nThere is network connection", color="\033[92m")
                    global modified_since_no_internet
                    if modified_since_no_internet:
                        download_file(args.input)
                        remove_files_not_in_file()
                        modified_since_no_internet = False
                    break
                except(TimeoutExpired):
                    count_expired+=10
                if not args.silent and count_expired % 10 == 0:
                    save(datetime.now().strftime("%d %b [%H:%M:%S] ") + "Trying to connect...")
                time.sleep(args.seconds)
        seconds = args.idle
        if seconds == 0:
            break
        if seconds < 60:
            save("Trying again in " + str(seconds) + " " + ("second" if seconds == 1 else "seconds"))
        elif seconds < 3600:
            save("Trying again in " + str(seconds/60) + " " + ("minute" if seconds == 60 else "minutes"))
        elif seconds < 86400:
            save("Trying again in " + str(seconds/3600) + " " + ("hour" if seconds == 3600 else "hours"))
        else:
            save("Trying again in " + str(seconds/86400) + " " +("day" if seconds == 86400 else "days"))

        time.sleep(args.idle)
        save("There is network connection")

class FileModifiedHandler(FileSystemEventHandler):

    def __init__(self, file_name):
        self.file_name = file_name

    def on_modified(self, event):
        # check if the file exists
        if not event.is_directory and event.src_path.endswith(self.file_name):
            save("[LOG] file " + self.file_name + " modified", color="\033[33m") # [LOG] in yellow
            download_file(self.file_name)
            remove_files_not_in_file()

def download_file(file_name):
    with open(file_name, "r") as urls:
        # add all links from the urls_to_download.txt file to the list_of_urls
        global list_of_urls
        list_of_urls = []
        for line in urls:
            # check if the line is a comment
            if line.strip().startswith("#"):
                pass
            elif line.strip() == "":
                # the line is empty
                pass
            else:
                url_to_download = line.strip()
                try:
                    response = urllib.request.urlopen(url_to_download)
                except(ValueError):
                    print("URL", url_to_download, "is not valid.")
                    continue
                except(HTTPError):
                    print("Cannot find web resource with", url_to_download, "url")
                    continue
                except(URLError):
                    # there is not internet connection
                    # set a flag indicating that the user modified the urls file after the internet went down
                    global modified_since_no_internet
                    modified_since_no_internet = True
                    continue

                webContent = response.read()

                # if the given output directory exists
                if os.path.isdir(args.out):
                    # get the hostname of the url
                    hostname = urllib.parse.urlparse(url_to_download).hostname
                    path = urllib.parse.urlparse(url_to_download).path.replace("/", "_")
                                                         # name of saved file
                    save_file_path = os.path.join(args.out, hostname + path) + ".html"
                    with open(save_file_path, "wb") as url_to_save:
                        # save the url
                        url_to_save.write(webContent)
                    list_of_urls.append(save_file_path)
                else:
                    print("The given output directory does not exist.")
                    break

def remove_files_not_in_file():
    if not os.path.isdir(args.out):
        return

    for root, dirs, files in os.walk(args.out):
        for file in files:
            file_with_path = os.path.join(args.out, file)
            global list_of_urls
                                                        # check if the file is an html file
            if file_with_path not in list_of_urls and file_with_path.rpartition('.')[-1] == "html":
                os.remove(file_with_path)
                print("[LOG] Removed", file_with_path)


def article_downloader():
    thread_current = threading.currentThread()
    observer = Observer()
    path = "."

    # populate the list of urls when the program starts
    for root, dirs, files in os.walk(args.out):
        for file in files:
            file_with_path = os.path.join(args.out, file)
            global list_of_urls
            if file_with_path not in list_of_urls and file_with_path.rpartition('.')[-1] == "html":
                list_of_urls.append(file_with_path)

    # download all resources on start of the program
    if os.path.isfile(args.input):
        download_file(args.input)
        remove_files_not_in_file()
                                            # file to watch
    watch_and_download = FileModifiedHandler(args.input)
    observer.schedule(watch_and_download, path, recursive=False)
    observer.start()
    while getattr(thread_current, "do_run", True):
        time.sleep(1)
    observer.stop()
    observer.join()

if not args.nodownload:
    # set up a thread for the watchdog process
    thread_watchdog = threading.Thread(target = article_downloader)
    thread_watchdog.start()

try:
    main()
except KeyboardInterrupt:
    save("\n\nGoodbye")
    if args.save != None:
        args.save.write("\n\n")
if args.save != None:
    args.save.write("---------------------------------------------------------------------------")
    args.save.close()

if not args.nodownload:
    thread_watchdog.do_run = False
    thread_watchdog.join()
sys.exit(0)

