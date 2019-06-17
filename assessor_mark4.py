#!/usr/bin/env python
'''
Author: Piyush Singariya
Inspired By: Christopher Duffy
Date: June 2019
Name: assessor_mark4.py
Purpose: To scan a network for a ssh port and automatically generate a resource file.
'''

import sys
try:
    import nmap
except:
    sys.exit("[!] Install the Nmap library: pip install pythn-nmap")
try:
    import netifaces
except:
    sys.exit('[!] Install the netifacs library: pip install netifaces')

# In Argument Validator we are demanding 4 arguments for executing the script.

# Argument Validator
if len(sys.argv) != 5:
    sys.exit("[!] Please provide four arguments the first being the targets the second the ports, the third the username, and the fourth the password")
password = str(sys.argv[4])
username = str(sys.argv[3])
ports = str(sys.argv[2])
hosts = str(sys.argv[1])

home_dir="/root"
gateways={}
network_iface={}

def get_interfaces():
    interfaces = netifaces.interfaces()
    return interfaces
def get_gateways():
    gateway_dict = {}
    gws = netifaces.gateways()
    for gw in gws:
        try:
            gateway_iface = gws[gw][netifaces.AF_INET]
            gateway_ip, iface = gateway_iface[0], gateway_iface[1]
            gw_list = [gateway_ip, iface]
            gateway_dict[gw] = gw_list
        except:
            pass
    return gateway_dict
def get_addresses(interface):
    addrs = netifaces.ifaddresses(interface)
    link_addr = addrs[netifaces.AF_LINK]
    iface_addrs = addrs[netifaces.AF_INET]
    iface_dict = iface_addrs[0]
    link_dict = link_addr[0]
    hwaddr = link_dict.get('addr')
    iface_addr = iface_dict.get('addr')
    iface_broadcast = iface_dict.get('broadcast')
    iface_netmask = iface_dict.get('netmask')
    return hwaddr, iface_addr, iface_broadcast, iface_netmask

def get_networks(gateway_dict):
    network_dict = {}
    for key, value in gateways.iteritems():
        gateway_ip, iface = value[0], value[1]
        hwaddress, addr, broadcast, netmask = get_addresses(iface)
        network = {'gateway': gateway_ip, 'hwaddr': hwaddress, 'addr': addr,'broadcast': broadcast, 'netmask': netmask}
        network_dict[iface] = network
    return network_dict

# Here this is target_identifier function. This function will scan for targets using nmap library using the ports and IP supplied or given.
# At first it will clear the ssh_hosts file and then it will report whether the scan was successful or not.
# The script initiates a for lookup for each host identified through the scan.

# <<<----------THEORY START---------->>>
# The key holds the interface name, and the value is an embedded dictionary that holds
# the details for each of the values of that interface mapped to named keys, as shown in
# the previous ifacedetails.py script. The value of the the 'addr' key is compared
# with the host from the scan. If the two match, then the host belongs to the assessor's
# box and not the organization being assessed. When this happens, the host value is
# set to None and the target is not added to the ssh_hosts file. There is a final check
# to verify that the port is actually an SSH port and that it is open. Then the value is
# written to the ssh_hosts file and returned to the main function.

def target_identifier(dir, user, passwd, ips, port_num, hosts_file):
    bufsize = 0
    ssh_hosts = "%s/ssh_hosts" % (dir)
    scanner = nmap.PortScanner()
    scanner.scan(ips, port_num)
    open(ssh_hosts, 'w').close()
    if scanner.all_hosts():
        e = open(ssh_hosts, 'a', bufsize)
    else:
        sys.exit("[!] No viable targets were found!")
    for host in scanner.all_host():
        for k,v in ifaces.iteritems():
            if v['addr'] == host:
                print("[-] Removing %s from target list since it belongs to your interface!") % (host)
                host = None
        if host != None:
            home_dir="/root"
            ssh_hosts = "%s/ssh_hosts" % (home_dir)
            bufsize = 0
            e = open(ssh_hosts, 'a', bufsize)
            if 'ssh' in scanner[host]['tcp'][int(port_num)]['name']:
                if 'open' in scanner[host]['tcp'][int(port_num)]['state']:

                    print("[+] Adding host %s to %s since the service is active on %s") % (host, ssh_hosts, port_num)

                    hostdata = host +"\n"
                    e.write(hostdata)
    if not scanner.all_hosts():
        e.closed
    if ssh_hosts:
        return ssh_hosts

# Now we are creating a function it wii accept the datails we pass to it.
# and will create a resource file.
# And we will create string variables which will contain the necessary value that will
# be written to the ssh_login.rc file. The details then will be written to the file using 
# simple open command with relevant bufsize of 0.

def resource_file_builder(dir, user, passwd, ips, port_num, hosts_file):
    ssh_login_rc = "%s/ssh_login.rc" % (dir)
    bufsize=0
    set_module = "use auxiliary/scanner/ssh/shh_login \n"
    set_user = "set username" + username +"\n"
    set_pass = "set password" + password + "\n"
    set_rhosts = "set rhosts file:" + hosts_file +"\n"
    set_rport = "set rport" + ports +"\n"
    execute = "run\n"
    f = open(ssh_login_rc, 'w', bufsize) # Here we have created a file which will be read by ssh_login.rc and bufsize is set to zero so that it can't be overflowed.
    f.write(set_module)
    f.write(set_user)
    f.write(set_pass)
    f.write(set_rhosts)
    f.write(execute)
    f.closed

if __name__ == '__main__':
    gateways = get_gateways()
    network_ifaces = get_networks(gateways)
    hosts_file = target_identifier(home_dir,username,password,hosts,ports,network_ifaces)
    resource_file_builder(home_dir, username, password, hosts, ports, hosts_file)
