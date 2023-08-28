#!usr/env python

import scapy.all as scapy
import argparse

def scan_ip(ip):

    # Creating arp request directed to broadcast MAC asking for IP
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Create an ethernet frame to use the MAC address to send the data and append our ip address later on. scapy.Ether()(Destination MAC address)
    arp_request_broadcast = broadcast/arp_request

    # Sending the package to the network and wait for response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] # srp allowed us to send a package with a custom ether, the package will go in the right direction becausewe added a ether layer to it

    # Parsing the response, extracting the data
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
        # print(element[1].psrc + "\t\t" +element[1].hwsrc); # psrc -> IP of the client that sent the package to us.  hwsrc (hardware source) -> MAC address of the client that send the package to us.
    return client_list
def print_result(client_list):
    print("IP\t\t\tMAC address\n----------------------------------------------");
    for client in client_list:
        print(client["ip"] + "\t\t" +client["mac"]);

def parser_handler():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="ip", help="Target IP and the range after '/'")
    opts = parser.parse_args()
    return opts

# scan_result = scan_ip("192.168.5.2/24") # /24 Allowed to go through all the range from 0 to 254

ops = parser_handler()
scan_result = scan_ip(ops.ip)
print_result(scan_result)