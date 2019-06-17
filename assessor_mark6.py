#!/usr/bin/env python
from scapy.all import *
ip = '192.168.195.1'
dst_port = 80
headers=IP(dst=ip)/TCP(dport=dst_port, flags="S")
answers,unanswers = sr(headers,timeout=10)

for a in answers:
    print(a[1][1].flags)

# We performed a SYN Scan and we should be looking for SYN+ACK Response.
# In TCP Flag a SYN response's positional value is 16 and ACK's value is 2 then overall value is 18.
