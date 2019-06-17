#!/usr/bin/env python
try:
    from scapy.all import *
except:
    sys.exit("[!] Install the scapy library using: pip install scapy")

ip = "127.0.0.1"
icmp = IP(dst=ip)/ICMP()
resp = sr1(icmp, timeout=10)

# Validation of Host is live or not.
if resp == None:
    print("The host is down")
else:
    print("The host is up")

# Checking for opening of Web port. To accomplish things like this we need to 
# execute a SYN scan.

answers,unanswers = sr1(icmp, timeout=10)

# sent, received = answers[80]