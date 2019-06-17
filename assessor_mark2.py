# Determining interface details with netfaces library
# This script uses a number of functions to accomplish specific tasks
# including get_networks, get_addresses, get_gateways and get_interfaces

import netifaces
import sys
try:
    import netifaces
except:
    sys.exit("[!] Install the netifaces library: pip install netifaces")

gateways = {}
network_ifaces={}

def get_interfaces():
    interfaces = netifaces.interfaces()
    return interfaces

# The second function identifies the gateways and return them as a dictionary

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

# The third function identifies the addresses for each interface

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

# This fourth fuction is actucally identifying the gateway IP from the dictionary provided 
# by the get_gateways function to the interface. 

def  get_networks(gateways_dict):
    networks_dict = {}
    for key, value in gateways.iteritems():
        gatteway_ip, iface = value[0], value[1]
        hwaddress, addr, broadcast, netmask = get_addresses(iface)
        network = {'gateway': gatteway_ip, 'hwaddr': hwaddress, 'addr': addr, 'broadcast': broadcast, 'netmask': netmask}
        networks_dict[iface] = network
    return networks_dict 

gateways = get_gateways()
network_ifaces = get_networks(gateways)
print(network_ifaces)