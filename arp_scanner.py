import scapy.all as scapy
import argparse

"""
steps to do arping :-
1. create arp request directed to broadcast mac asking for i
p
1.1 create arp to ask who has target ip.
1.2 set destination mac to broadcast mac

2. send packets and recieve responce
3. parse the responce
4. print result
"""

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="ip",help="Target IP / IP range")
    options = parser.parse_args()
    if not options.ip:
        parser.error("[-] Please specify the ip address")
    return options

def scan_automatic(ip):
    scapy.arping(ip)

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    clients_list = []
    for element in answered_list:
        clients_list.append({"ip":element[1].psrc,"mac":element[1].hwsrc})

    return clients_list

def print_result(results_list):
    print("IP\t\tMAC Address\n---------------------------------------------------")
    for element in results_list:
        print(element["ip"]+"\t"+element["mac"])

ip = get_arguments().ip
scan_result = scan(ip)
print_result(scan_result)

