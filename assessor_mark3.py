#!/etc/bin/env python

# This script is an Nmap Scanner

#<-----------Author: Piyush Singariya----------->#
#<-----------Date: June 2019----------->#
#<-----------Name: assessor_mark3.py----------->#
#<-----------Purpose: To scan a network----------->#

import sys
try:
    import nmap
except:
    sys.exit("[!] Install the nmap library using: pip install python-nmap")

# nmap libraries have been imported because we are creating a nmap scanner
# and we are importing sys library to use CLI.

# Once we have imported our sweet sweet libraries now script can have argument requirement designed.
#  We need at least two arguments. If script will have less or more than two than script
# should fail and should leave a message behind

#<---------Argument Validator------------>#

if len(sys.argv) !=3:
    sys.exit("Please provide two arguments the first being the targets and second as the ports")
ports = str(sys.argv[2])
addrs = str(sys.argv[1])

scanner = nmap.PortScanner()
scanner.scan(addrs, ports)
for host in scanner.all_hosts():
    if not scanner[host].hostname():
        print("The host's IP address is %s and it's hostname was not found.") % (host)
else:
    print("The host's IP address is %s and it's hostname is %s") % (host, scanner[host].hostname())
