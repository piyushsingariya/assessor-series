#!/usr/bin/env python
'''
Author: Piyush Singariya
Date: June 2019
Name: assessor_mark12.py(httplib2_brute.py)
Purpose: Prototype code that allows you to build a multiple request response train with the httplib2 library'''

import urllib, httplib2, argparse, sys

def host_test(users, passes, target):
    with open(users) as f:
        usernames = f.readlines()
    with open(passes) as g:
        passwords = g.readlines()
    http = httplib2.Http()
    http.follow_redirects = True
    for user in usernames:
        for passwd in passwords:
            header = {'Content-type': 'application/x-www-form-urlencoded'}
            parameters = {'username' : user.rstrip('\n'), 'password':passwd.rstrip('\n'), 'Submit':'Login'}
            print("[*] Testing username %s and password %s against %s") % (user.rstrip('\n'), passwd.rstrip('\n'), target.rstrip('\n'))
            response, content = http.request(target, 'POST', headers=header, body=urllib.urlencode(parameters))
            print("[*] The response size is: %s") % (len(content))
            print("[*] The cookie for this attempt is: %s") % (str(response['set-cookie']))

def main():
    # If script is executed at the CLI
    usage = '''usage: %(prog)s [-t http://127.0.0.1] [-f wordlist] -q -v -vv -vvv'''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-t", action="store", dest="target", default=None, help="Host to test")
    parser.add_argument("-u", action="store", dest="username", default=None, help="Filename of usernames to test for")
    parser.add_argument("-p", action="store", dest="password", default=None, help="Filename of passwords to test for")
    parser.add_argument("-v", action="count", dest="verbose", default=1, help="Verbosity level, defaults to one, this outputs each command and result")
    parser.add_argument("-q", action="store_const", dest="verbose", const=0, help="Sets the results to be quiet")
    parser.add_argument('--version', action='version', version='%(prog)s 0.42b')
    args = parser.parse_args()

    # Argument Validator
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    if (args.target == None) or (args.password == None) or (args.username == None):
        parser.print_help()
        sys.exit(1)

    # Set Constructors
    verbose = args.verbose     # Verbosity level
    username = args.username   # The password to use for the dictionary attack
    password = args.password   # The username to use for the dictionary attack
    target = args.target       # Password or hash to test against default is admin

    host_test(username, password, target)

if __name__ == '__main__':
    main()
