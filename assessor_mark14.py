#!/usr/bin/env python
try:
    import tftpy
except:
    sys.exit("[!] Install the package tftpy with: pip install tftpy")
def main():
    ip = "192.168.195.165"
    port = 69
    tclient = tftpy.TftpClient(ip,port)
    for inc in range(100):
        filename = "exapmle_router" + "-" + str(inc)
        print("[*] Attempting to download %s from %s:%s") % (filename, ip, port)
        try:
            tclient.download(filename, filename)
        except:
            print("[-] Failed to download %s from %s:%s") % (filename, ip, port)

if __name__ == "__main__":
    main()