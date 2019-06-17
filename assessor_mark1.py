#!/usr/bin/env python

'''
Author: Piyush Singariya
Inspiration: Christopher Duffy
Purpose: To grab your current Public IP (Ethernet & Wireless Lan), Private IP, MAC Addresses, Fully Qualified Domain Name, and Hostname
Name: assessor_mark1.py

This PythonX Script should be used on your own. Author isn't responsible
for any acts against laws using this Script. This Script is just created for Educational Purpose and to practice more and more.
Many of the things isn't explainable that's why I didn't explained. Right now I am still in learning May be in future I will write a full write-up explaining 
this whole program including it's arguments, functions, parameters, variable everything.
If you are watching this may be you can suggest edits and advancements to this script.
mailto:piyushsingariya@gmail.com
''' 




import socketserver
import socket
import os
import subprocess
import shutil
import errno
if os.name != "nt":
    import fcntl
import urllib2
import struct
import uuid

# The first function is called get_ip . It takes an
# interface name and then tries to identify an IP address for that interface

def get_ip(inter):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', inter[:15]))[20:24])
    return ip_addr


# The second function, called get_mac_address , identifies the MAC address of a
# specific interface

def get_mac_address(inter):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s',inter[:15]))
    mac_address = ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
    return mac_address

# The third function gets the details of the host and returns them to the main part
# of the script.

def get_localhost_details(interfaces_eth, interfaces_wlan):
    host_data = "None"
    hostname = "None"
    windows_ip = "None"
    eth_ip = "None"
    wlan_ip = "None"
    host_fqdn = "None" # Fully Qualified Domain Name (FQDN)
    eth_mac = "None"
    wlan_mac = "None"
    windows_mac = "None"
    hostname = socket.gethostbyname(socket.gethostname())
    if hostname.startswith("127.") and os.name != "nt" :
        hostdata = socket.gethostbyaddr(socket.gethostname())
        hostname = socket.getfqdn()
        for interface in interfaces_eth:
            try:
                eth_ip = get_ip(interface)
                if not "None" in eth_ip:
                    eth_mac = get_mac_address(interface)
                break
            except IOError:
                pass
        for interface in interfaces_wlan:
            try:
                wlan_ip = get_ip(interface)
                if not "None" in wlan_ip:
                    wlan_mac = get_mac_address(interface)
                break
            except IOError:
                pass
    else:
        windows_ip = socket.gethostbyname(socket.gethostbyname())
        windows_mac = hex(getnode()).lstrip('0x')
        windows_mac = ':'.join(pos1+pos2 for pos1,pos2 in zip(windows_mac[::2],windows_mac[1::2]))
        hostdata = socket.gethostbyaddr(socket.gethostbyname())
        hostname = str(hostdata[1].strip("[]\'"))
        host_fqdn = socket.getfqdn()
    return hostdata, hostname, windows_ip, eth_ip, wlan_ip, host_fqdn, eth_mac, wlan_mac, windows_mac

# The final function in this script is called get_public_ip , which queries a known
# website for the IP address that is connected to it. This IP address is returned to
# the web page in a simple, raw format. There are a number of sites against which
# this can be done, but make sure you know the acceptable use and terms of service
# authorized.

def get_public_ip(request_target):
    grabber = urllib2.build_opener()
    grabber.addheader = [{'User-agent','Mozilla/5.0'}]

    try:
        public_ip_address = grabber.open(target_url).read()
    except urllib2.HTTPError, error:
        print("There was an error trying to get your Public IP: %s") % (error)
    except urllib2.URLError, error:
        print("There was an error trying to get your Public IP: %s") % (error)
    return public_ip_address    

wireless_ip = "None"
windows_ip = "None"
ethernet_ip = "None"
public_ip = "None"
host_fqdn = "None"
hostname = "None"
fqdn = "None"
ethernet_mac = "None"
wireless_mac = "None"
windows_mac = "None"
target_url = "http://ip.42.pl/raw"
inter_eth = ["eth0","eth1","eth2","eth3"]
inter_wlan = ["wlan0","wlan1","wlan2","wlan3","wifi0","wifi1","wifi2","wifi3","ath0","ath1","ath2","ath3"]

public_ip = get_public_ip(target_url)
hostdata, hostname, windows_ip, ethernet_ip, wireless_ip, host_fqdn, ethernet_mac, wireless_mac, windows_mac = get_localhost_details(inter_eth, inter_wlan)

if not "None" in public_ip:
    print("Your Public IP address is : %s") % (str(public_ip))
else:
    print("Your Public IP address was not found.")

if not "None" in ethernet_ip:
    print("Your Ethernet IP address is: %s") % (str(ethernet_ip))
    print("Your Ethernet MAC address is: %s") % (str(ethernet_mac))
elif os.name != "nt":
    print("No active Ethernet Device was found.")

if not "None" in wireless_ip:
    print("Your Wireless IP address is: %s") % (str(wireless_ip))
    print("Your Wireless Device MAC Address is: %s") % (str(wireless_mac))
elif os.name == "nt":
    print("No active Wireless Device was found.")

if not "None" in windows_ip:
    print("Your Windows IP address is: %s") % (str(windows_ip))
    print("Your Windows MAC Address is: %s") % (str(windows_mac))
else:
    print("You are not running Windows.")

if not "None" in hostname:
    print("Your System's hostname is: %s") % (str(hostname))

if host_fqdn == 'localhost':
    print("Your System is not Registered to a Domain.")
else:
    print("Your System's Fully Qualified Domain Name is: %s") % (host_fqdn)
