#!/usr/bin/python
#
# bsparser copyright (C) 2013 rbsec
# Licensed under GPLv3, see LICENSE for details
#

import base64
import re
import platform
import os
import sys
import urlparse

try:    # Use faster C implementation if we can
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

try:
    import argparse
except:
    print("FATAL: Module argparse missing (python-argparse)")
    sys.exit(1)


class output:
    def status(self, message):
        print(col.blue + "[*] " + col.end + message)

    def good(self, message):
        print(col.green + "[+] " + col.end + message)

    def verbose(self, message):
        if args.verbose:
            print(col.brown + "[v] " + col.end + message)

    def warn(self, message):
        print(col.red + "[-] " + col.end + message)

    def fatal(self, message):
        print("\n" + col.red + "FATAL: " + message + col.end)


class col:
    if sys.stdout.isatty() and platform.system() != "Windows":
        green = '\033[32m'
        blue = '\033[94m'
        red = '\033[31m'
        brown = '\033[33m'
        end = '\033[0m'
    else:   # Colours mess up redirected output, disable them
        green = ""
        blue = ""
        red = ""
        brown = ""
        end = ""

def generate_pagelist():
    pagelist = set()
    out.verbose("Opening input file " + args.infile)
    for event, elem in ET.iterparse(args.infile):
        if event == 'end':
            if elem.tag == 'url':
                u = str(elem.text)
                url = urlparse.urlsplit(u)
                if url.path.lower().endswith('php'):
                    pagelist.add(url.path)
#            if elem.tag == 'response':
#                if elem.attrib["base64"] == "true":
#                    response = str(base64.b64decode(elem.text))
#                else:
#                    response = str(elem.text)
#                words = re.findall("[a-zA-Z0-9\-]+", response)
#                for word in words:
#                    wordlist.add(word)
        elem.clear() # Discard the element to free memory

    pagelist = sorted(pagelist, key=lambda s: s.lower())    # Case insensitive sort
    f = open(args.pagelist, "w")
    for page in pagelist:
        f.write(page + "\n")
    out.good("Wrote " + str(len(pagelist)) + " words to " + args.pagelist)

def generate_wordlist():
    wordlist = set()
    out.verbose("Opening input file " + args.infile)
    for event, elem in ET.iterparse(args.infile):
        if event == 'end':
            if elem.tag == 'response':
                if elem.attrib["base64"] == "true":
                    response = str(base64.b64decode(elem.text))
                else:
                    response = str(elem.text)
                words = re.findall("[a-zA-Z0-9\-]+", response)
                for word in words:
                    wordlist.add(word)
        elem.clear() # Discard the element to free memory
    wordlist = sorted(wordlist, key=lambda s: s.lower())    # Case insensitive sort
    f = open(args.wordlist, "w")
    for word in wordlist:
        f.write(word + "\n")
    out.good("Wrote " + str(len(wordlist)) + " words to " + args.wordlist)


def get_args():
    global args
    parser = argparse.ArgumentParser('bsparser.py', formatter_class=lambda prog:argparse.HelpFormatter(prog,max_help_position=40))
    parser.add_argument('-i', '--input', help='Input file', dest='infile', required=True)
    parser.add_argument('-p', '--pagelist', help='Generate pagelist', dest='pagelist', required=False)
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help='Verbose', dest='verbose', required=False)
    parser.add_argument('-w', '--wordlist', help='Generate wordlist', dest='wordlist', required=False)
    args = parser.parse_args()

if __name__ == "__main__":
    global wildcard
    out = output()
    get_args()
    if args.wordlist:
        generate_wordlist()
    if args.pagelist:
        generate_pagelist()

