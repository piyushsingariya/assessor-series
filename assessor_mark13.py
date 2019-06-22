#!/usr/bin/env python
import socket

def main():
    ports = [21,23,22]
    ips = "192.168.195." 
    for octet in range(0,225):
        for port in ports:
            ip = ips + str(octet)
            # Print ("[*] Testing port %s at IP %s") % (port, ip)
            try:
                socket.setdefaulttimeout(1)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip,port))
                output = s.recv(1024)
                print("[+] The banner: %s for IP: %s at Port: %s") % (output,ip,port)
            except:
                print("[-] Failed to connect to %s:%s") % (ip, port)
            finally:
                s.close()

if __name__ == "__main__":
    main()