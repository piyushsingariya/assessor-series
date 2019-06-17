#!/usr/bin/env python

'''
Author: Piyush Singariya
Date: June 2019
Name: assessor_mark10.py(dirtester.py)
Purpose: To identify unlinked and hidden files or directories within web applications'''


import urllib, argparse, sys

def host_test(filename, host):
    file = 'headrequests.log'
    bufsize = 0
    e = open(file, 'a', bufsize)
    print("[*] Reading file %s") % (file)
    with open(filename) as f:
        locations = f.readlines()
    for item in locations:
        target = host + "/" + item
        try:
            request = urllib.Request(target)
            request.get_method = lambda : 'GET'
            response = urllib.urlopen(request)
        except:
            print("[-] %s is invalid") % (str(target.rstrip()))
            response = None
        if response != None:
            print("[+] %s is valid") % (str(target.rstrip()))
            details = response.info()
            e.write(str(details))
    e.close

def main():
    # If script is executed at the CLI
    usage = '''usage: %(prog)s [-t http://127.0.0.1] [-f wordlist] -q -v -vv -vvv'''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-t", action="store", dest="target", default=None, help="Host to test")
    parser.add_argument("-f", action="store", dest="filename", default=None, help="Filename of directories or pages to test for")
    parser.add_argument("-v", action="count", dest="verbose", default=1, help="Verbosity level, defaults to one, this outputs each command and result")
    parser.add_argument("-q", action="store_const", dest="verbose", const=0, help="Sets the results to be quiet")
    parser.add_argument('--version', action='version', version='%(prog)s 0.42b')
    args = parser.parse_args()

    # Argument Validator
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    if (args.target == None) or (args.filename == None):
        parser.print_help()
        sys.exit(1)

    # Set Constructors
    verbose = args.verbose     # Verbosity level
    filename = args.filename # The data to use for the dictionary attack
    target = args.target       # Password or hash to test against default is admin

    host_test(filename, target)

if __name__ == '__main__':
    main()